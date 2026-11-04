# 模型選擇：專用 DGX Spark 的容量與能力取捨

回到 [逐步部署](README.md)。此選型假設 **單台 128 GB DGX Spark 專做 inference**，其他機器負責 KG／agent。查閱日期：2026-10-26；尚無本專案真實資料的模型成效或 Spark 效能實測。

## 建議順序

### 專用推論伺服器的選型決策

依你的分工，Spark 不需替 KG、agent 或資料處理預留應用程式資源，因此不再以 3B–8B 為容量上限。建議把「可重現的部署基線」與「能力升級候選」都納入第一輪選型：先讓 27B BF16 通過服務驗收，再優先測試 122B-A10B NVFP4；32B BF16 用作另一個 dense 對照。122B 若在開發錄製上的惡意 recall、誤報與證據支持率較好，且單事件延遲可接受，就升為正式 backbone，不必為了維持 SLM 名稱而縮小模型。

專用服務仍須保留 OS、推論 workspace 與 cache 的記憶體。第一輪讓多台 client 共用一個模型服務、由 client 排隊，並行數先設為 1；完成最長請求測試後才提高到 2。多台機器能連線不等於 GPU 必須同時執行所有請求。這樣可把容量優先用於較大模型，而不是一開始就追求高併發。

「較大參數」是值得驗證的能力假設，不能保證本研究的 malicious 判別一定較好。尤其 27B BF16 與 122B NVFP4 同時改變架構和量化，應視為部署方案比較；若要推論純粹的參數規模效應，還需另設控制條件。所有候選使用相同開發錄製、KG snapshot、上下文與工具預算，選定後凍結版本再跑測試錄製。

**先部署 Qwen3.5-27B BF16 作能力優先的基線。** 它是 27B dense 模型，具指令／工具使用能力，允許本地部署。本研究先使用文字輸入與 non-thinking 模式，讓每輪輸出及成本容易控制。此推薦基於任務適配、可管理的記憶體需求與可重現性，不宣稱它是目前所有模型中最強。[官方模型卡](https://huggingface.co/Qwen/Qwen3.5-27B)

原本的 3B–8B 不再限制主模型。27B／32B 都應記錄為新的 backbone 條件；如果論文仍稱 SLM，需清楚交代參數規模，不能把模型變大帶來的改善歸因於 KG。

| 定位 | 精確模型 ID | 精度 | 選擇理由與限制 |
|---|---|---|---|
| **主線** | `Qwen/Qwen3.5-27B` | BF16 | 中大型 dense 模型，先保留權重精度；混合 attention／DeltaNet 需要通過 Spark kernel 驗收 |
| **第二模型／相容性對照** | `Qwen/Qwen3-32B` | BF16 | 純文字 dense 模型，可對照不同架構／訓練版本；參數較多不代表一定勝過 27B |
| **較新、偏服務效率候選** | `nvidia/Qwen3.8-27B-NVFP4` | NVFP4 | NVIDIA 現行 Spark playbook 有對應 recipe；精度與模型版本同時變動，需獨立成組 |
| **更大容量探索** | `nvidia/Qwen3.5-122B-A10B-NVFP4` | NVFP4 | 122B 總參數、每 token 約 10B activated 的 MoE；必須另驗證 GB10 的量化／MoE kernels 與延遲 |

這些 repository 模型卡標示 Apache-2.0，下載時仍保存該 revision 的 LICENSE。開放權重與授權不代表所有訓練資料可重建。[Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B)、[Qwen3.8 量化版](https://huggingface.co/nvidia/Qwen3.8-27B-NVFP4)、[122B 量化版](https://huggingface.co/nvidia/Qwen3.5-122B-A10B-NVFP4)

不把 coding 專用模型列為第一主線：此任務主要是事件理解、依證據判別與工具選擇，通用 instruction 模型更直接對應研究問題。這是研究設計判斷，並非已量測的 coding 模型劣勢。

## 記憶體：能載入不等於能穩定服務

下表僅以 `參數數量 × 每參數 bytes` 估算**理想權重本體**，使用十進位 GB，未含 scale／metadata、未量化層、視覺組件、KV／recurrent cache、workspace、容器與作業系統：

| 模型規模／格式 | 權重本體粗估 | 對單台 128 GB Spark 的判斷 |
|---|---:|---|
| 27B BF16 | 約54 GB | 合理的第一個實機驗證目標，有空間留給 runtime 與短 context |
| 32B BF16 | 約64 GB | 可作下一組候選，較少記憶體餘裕 |
| 27B FP4 | 約13.5 GB | 實際 checkpoint 大於這個理想值；可換取併發／cache 空間 |
| 122B FP4 | 約61 GB | 容量上值得驗證，仍須加上量化 metadata 與非 FP4 層 |
| 122B FP8 | 約122 GB | 幾乎耗盡總容量，不作單台服務主線 |
| 70B BF16 | 約140 GB | 超過此機器總容量，不採用 |

122B-A10B 的 A10B 指 activated parameters，不能只按 10B 算載入記憶體。單機一般仍需保存全部 experts。dense／MoE 的參數量也不是等價能力或等價運算量指標。

Spark 的 128 GB 是 CPU/GPU 共享；低位元 peak FLOPS 不是 BF16 解碼速度。記憶體頻寬、實際讀取權重、kernel、上下文長度和併發會共同影響延遲。因此沒有在此文件承諾 tok/s 或「200B 一定可用」之類部署效能。

## 為何第一版先採 BF16

專用 Spark 有機會在保留短 context 餘裕下運行 27B BF16，先建立未低位元量化的參考點。之後比較同模型 BF16／FP8／NVFP4 時，才能分辨精度變化的影響。記憶體節省或 throughput 改善不能代替惡意 recall、誤報與引用正確性的驗證。

如果你的首要目標是提高服務併發，可優先試官方 Spark recipe 的 Qwen3.8-27B NVFP4。它與主線不同模型／精度，結果應標為新條件。NVIDIA 現行 recipe 也使用 speculative decoding 的 draft model；首輪宜關閉這個額外變因，或將 draft revision 一併鎖定。[Spark 官方候選與配套容器](https://build.nvidia.com/spark/vllm/intermediate)

## 32B BF16 如何切換

保留原部署資料，新建一個 state 目錄，重新執行 README 步驟 2–5，但下載改成 `--repo Qwen/Qwen3-32B`。Spark 同時間先只服務一個大模型。

```bash
# [Spark] 先保存舊服務的 logs 與設定，再停止該服務
docker stop ants-registry-slm
# 指向已完成下載／image digest／API key 設定的 32B state
export SLM_STATE="$HOME/ants-slm/qwen3-32b-bf16-v1"
export SPARK_BIND_IP="192.168.50.10"
export SLM_MODEL_FAMILY=qwen3
export SLM_CONTAINER_NAME=ants-registry-slm-32b
export SLM_MAX_NUM_SEQS=1
bash "$HOME/slm_depoly/scripts/serve.sh" --dry-run
bash "$HOME/slm_depoly/scripts/serve.sh"
```

啟動後重新完成 client probes。Qwen3 仍需在每個 request 設定 `chat_template_kwargs.enable_thinking=false`；不得混用不同的 thinking 狀態。32B 服務亦使用相同 `registry-slm` 別名，所以實驗端必須額外保存真實 repo／revision，不能只記錄 API alias。

## 若要進一步試 122B

這是**進階候選與待驗證路線**，不是本目錄 BF16 launcher 已支援的配置：

1. 使用 `download_model.py --repo nvidia/Qwen3.5-122B-A10B-NVFP4 --dest <新目錄>` 鎖定 checkpoint。
2. 查閱該 checkpoint 的 `quantization_config`、官方模型卡與當時的 Spark／GB10 對應 recipe。NVIDIA 模型卡列 Blackwell／vLLM；這本身不足以證明所有 Blackwell GPU、所有容器版本均相容。
3. 確認 **Arm64、SM121、MoE、NVFP4 GEMM** 在同一環境可用。不要把 B200 的設定直接視為 GB10 的設定。
4. 使用該 recipe 的量化後端，固定 image digest，從 TP=1、8K context、concurrency=1 開始。NVFP4 checkpoint 不應被強制轉成普通 BF16 權重。
5. 保留 system memory 餘裕，完整執行 JSON、工具動作、長輸入與穩定性驗收。若無匹配 kernel，回到已驗收模型，不透過任意提高 memory fraction 掩蓋問題。
6. 在同一個開發集、同一證據與 agent 預算下比較 27B／122B。只有在品質或品質／成本取捨更合適時升級。

若研究目標是「以固定 KG 支援能力較強的本地模型」，27B／32B 已是合理主線；若要研究 scaling，需將小模型、大模型、量化和 KG 作為分開的實驗因素。

## 模型選定準則

先用合成題測框架，再用預先劃定的開發錄製選模型與設定：格式／工具合法率、證據支持率、balanced class recall、誤報、拒答、p95 延遲、tokens／事件。不能根據最終測試成績選「最佳模型」後仍宣稱盲測。

初版保留 non-thinking 的 512 output-token 預算。要測 thinking，另設足夠的輸出／推理預算並重新報成本；512 token 截斷的 thinking 模型不能用來公平比較能力。更大參數與更多 thinking 都需要實測，不自動視為正確判別的保證。
