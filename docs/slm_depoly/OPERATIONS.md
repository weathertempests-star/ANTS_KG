# 實機驗收、維運與排錯

回到 [部署主線](README.md)／[Client 指引](CLIENT_AND_EXPERIMENT.md)。以下均為部署後需實際執行的檢查，不是本次已取得的 Spark 測試結果。

## 驗收階梯

1. **環境**：Arm64 容器、GPU 可見、BF16 CUDA 基本運算成功。
2. **載入**：27B 模型啟動、無持續 OOM／kernel error、啟動參數與 digest 保存。
3. **網路**：核准 client 可連接；未核准來源被 ACL 阻擋；`/v1/models` 不帶 key 應拒絕，正確 key 成功。健康端點成功不能代替認證驗收。
4. **格式**：三個 probes 完成，finish_reason 正常、schema 與引用合法、有 usage。
5. **負載**：用合成或開發資料覆蓋短輸入、約4K輸入、接近512輸出、1／2併發。保存超時、錯誤、峰值記憶體與 p50/p95 延遲。
6. **研究契約**：Client 能限制資訊、工具與預算；正確處理未判定／失敗。完成後才執行凍結的真實資料評估。

附帶 probe 可先重複10輪測基本穩定性：

```bash
# [Client] 使用 Client 指引中的變數
"$SLM_CLIENT_STATE/venv/bin/python" docs/slm_depoly/scripts/probe_server.py \
  --base-url "$SLM_BASE_URL" --allow-lan --repeat 10 \
  --out "$SLM_CLIENT_STATE/probe-repeat-001"
```

這是30次短請求、循序執行，不是長 context／併發 benchmark。第一輪包含 warm-up／schema 編譯影響，獨立標記；不能把這組延遲直接推算到全部真實事件。

## 初始調校順序

每次只改一項，保留新設定與 probe 目錄：

1. 啟動不穩先設 `SLM_MAX_NUM_SEQS=1`；仍失敗時依 log 分辨 kernel、權重載入或 cache 問題。
2. 確認128GB配置與其他程序佔用，再調 memory fraction。比例增大會減少系統餘裕，不是通用 OOM 解法。
3. 穩定後比較 eager 與 CUDA graph；移除 `--enforce-eager` 需修改 launcher 的版本副本並重新凍結，不直接改已用於實驗的配置。
4. 再測 prefix caching，分開報冷／熱 cache；schema／模型編譯 warm-up 也記錄。
5. 再測併發1→2→4。多 client 要用全域提交限制，避免每台都各自送4個請求導致大量排隊。
6. 最後才測量化、MTP／speculative decoding，另存模型／draft revision與設定，重跑品質驗證。

紀錄每個請求的輸入／輸出 tokens、整體端到端 latency、錯誤和重試。非串流 API 只有總延遲，不能把它叫 TTFT；如需 TTFT，另外實作 streaming 計時。不要用錄製 log 的 timestamp 計算推論延遲。

估算整體實驗時間時，以實測整個 agent 的平均耗時／完成目標吞吐乘上目標數及比較條件，另計重試。agent 每事件可能多次呼叫，不能只用模型生成 tok/s 當整個研究吞吐。

## 常見問題

| 現象 | 檢查與處理 |
|---|---|
| `exec format error` | image architecture 應為 arm64；重新拉對應平台並鎖 digest |
| `torch.cuda.is_available() == False` | host driver、NVIDIA Container Runtime、`--gpus all`；先修環境 |
| driver insufficient／CUDA mismatch | 容器 CUDA 與 host driver 不相容；依原廠更新指南選匹配組合 |
| `no kernel image`、SM121 或 DeltaNet／Triton kernel error | 不代表模型容量不足；確認此 image 支援 GB10 與模型 architecture；用對應 Spark recipe／新鎖定 image，或試32B對照 |
| 不認識 `qwen3_5`／tokenizer | image 中 transformers／vLLM 太舊或模型錯誤；核對 runtime versions，勿在運行容器隨意 pip upgrade |
| 權重載入 OOM | 看系統 free memory、模型是否誤選BF16的122B、是否同時啟動其他大模型 |
| cache不足／最大長度檢查失敗 | 降低服務 context 或併發，檢查引擎實際 cache 配置；與純權重 OOM 分開處理 |
| localhost能通、Client不通 | 本主線只綁LAN IP；檢查 bind address、route、ACL、防火牆與實際listen；不要靠全開port解決 |
| HTTP401 | Client key與server env不一致、key含換行、使用錯的服務；probe讀檔會去除尾端空白 |
| HTTP400 schema／參數錯誤 | 保存error body；對照鎖定版本API。不要無聲刪除response_format假裝通過 |
| `<think>`／reasoning佔滿輸出 | 確認每次request都含enable_thinking=false；不可只在文字提示寫「不要思考」 |
| `finish_reason=length` | 輸出被截斷；記為失敗，在開發階段縮短答案schema或另設預算版本 |
| JSON合法卻引用不存在ID | Client拒絕或依預定修復政策處理；schema不保證證據正確 |
| probe下載依賴失敗 | 檢查下載端網路／proxy；推論端offline模式不負責安裝依賴 |
| port／container name已被使用 | 先辨識既有服務；只停止自己的容器，保留狀態，不批次刪除 |

## 停止、恢復與開機重啟

```bash
# [Spark] 使用目前服務名稱；若切到32B請改名
docker logs ants-registry-slm > "$SLM_STATE/metadata/server.log" 2>&1
docker stop ants-registry-slm
docker start ants-registry-slm
```

`start` 重用原容器的模型掛載、key與參數。若需要換參數，保存舊命令／日誌後停止舊容器，再以新名稱建立新容器；不要把舊state目錄改成另一個模型。首次驗收後如需開機恢復：

```bash
# [Spark] 確定服務已穩定且Docker會隨系統啟動
docker update --restart unless-stopped ants-registry-slm
```

## 內網加密選項

主線是受ACL限制的內網HTTP。API key提供驗證，HTTP不提供機密性。需要加密時選一種：

- 使用實驗室TLS reverse proxy，核准client來源，驗證bearer token，只公開需要的路由，設定非必要路由拒絕；後端vLLM綁loopback。
- 使用vLLM的`--ssl-keyfile`、`--ssl-certfile`與實驗室簽發的憑證，Client使用HTTPS及受信任CA，保留同樣ACL；不要用忽略憑證驗證當正式設定。
- 單一研究者可用SSH tunnel，無需公開模型API到整個網段：

```bash
# [Client] 後端原本綁在Spark LAN IP
ssh -N -L 18000:192.168.50.10:8000 spark-user@192.168.50.10
# 另一個Client shell：export SLM_BASE_URL=http://127.0.0.1:18000
```

tunnel仍使用原API key；probe對loopback不需`--allow-lan`。多使用者長期服務宜採實驗室管理的TLS／ACL與key輪替。官方文件說明vLLM的API key不涵蓋所有路由，所以不能只驗證`/v1`就認為整個port皆受保護。[vLLM服務參數](https://docs.vllm.ai/en/v0.28.0/cli/serve/#--api-key)

## 可交付驗收紀錄

最終保存：硬體／driver資訊、image digest、模型與tokenizer lock、server command、三類probe結果、長輸入與併發量測、失敗分類、可連線與拒絕來源驗證、Client端protocol版本。API key檔案不列入可分享報告。

目前提供的launcher與probe是部署輔助工具；通過這些工程驗收後，仍須依研究計畫測量真實log的判別能力，才能聲稱較大模型或KG改善效果。
