# 研究機器連接專用 Spark 模型伺服器

DGX Spark 只執行推論服務。資料、KG、agent、工具、checkpoint 與人工答案都由研究機器保存。模型提出的工具動作由此程式驗證並在本機執行，不在 Spark 執行任意程式。

## 安裝 client

Python 3.10+。核心僅使用標準函式庫，可直接在專案根目錄執行 `python -m ants_kgmaer`。若要安裝 console entry point：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/ants-kgmaer --help
```

在有 setuptools>=61 與 wheel 的環境，也可離線建置：

```bash
python3 -m pip wheel . --no-deps --no-build-isolation --no-index --wheel-dir dist
```

初次無建置工具時仍需由套件來源取得 setuptools/wheel。核心不需要 GPU、PyTorch 或模型權重。`pip install '.[agent]'` 安裝選用 LangGraph；native 與 LangGraph 共用同一有界 session，但後者目前尚未通過此環境的 runtime 驗收。

## 凍結實際部署身分

將 `configs/spark-agent.template.json` 複製為自己的設定檔，替換 LAN 位址與部署後取得的完整 model revision、tokenizer revision、image digest。範本故意包含會被拒絕的 placeholder，不能把假 SHA 當成實測部署身分。若改成 32B 或 122B 模型，也必須同步記錄實際 repo、revision 與精度。

`base_url` 是 origin，例如 `http://192.168.50.10:8000`，不加 `/v1`。程式只接受 loopback 或 private LAN literal IP，停用 proxy 與 redirect。API key 放在 `SLM_API_KEY_FILE` 指向的本機檔案，或 `SLM_API_KEY` 環境變數；不寫入 JSON 設定。非 loopback 位址必須提供 key。

```bash
export SLM_API_KEY_FILE="$HOME/ants-client/api.key"
python -m ants_kgmaer run \
  --config configs/my-spark-agent.json \
  --dataset workspaces/recordings-v1 --selection workspaces/pilot-v1 \
  --output runs/spark-engineering-v1
```

服務需提供 `/health`、`/v1/models`、`/tokenize`、`/v1/chat/completions`，並支援 JSON Schema 輸出與關閉 thinking 的 chat template 設定。Client 使用服務端 tokenizer 計算包含 schema 的實際 prompt tokens；無法計數時明示失敗，不退回字元估計。模型 alias 只驗證服務名稱，不能證明權重 revision；部署 lock 仍須由操作者核對保存。

範本限制 200 個目標作工程測試。它們是選樣清單順序的前 200 個，不代表每份錄製都被涵蓋。完成框架驗收並凍結設定後，另建正式設定與 run，移除 `engineering_limit`；也須確認來源 split 與研究宣稱符合實際開發過程。沒有實際 Spark 端點前，不能填報吞吐或偵測能力。

## 次要動態歷史實驗

主比較固定 `history_k=0` 或 `16`，不由 agent 決定是否看歷史。次要研究可設 `condition=agent`、`history_k=0`、`dynamic_history=true`，開放 `get_prior_context(k)`，上限 16。只能揭露預先計算的同錄製、同程序、嚴格先前事件；同排序值沒有已知先後。候選池固定，模型不能指定檔案、時間區間或任意事件 ID。

批次內可見 ID 在呼叫前凍結：同一輪取得的歷史只能在下一輪被 `lookup_registry` 引用。恢復執行與 replay 保留相同別名、歷史與已用額度。此條件改變歷史取得政策，應獨立報告，不能直接把相對固定 K=0 的提升全部歸因於 KG。

## 驗收狀態

目前已驗證核心單元／mock 流程與離線 wheel 的內附 KG 載入。此環境不允許 socket，因此 loopback HTTP 測試仍未完成；真實 Spark、LangGraph runtime 與模型品質也尚未驗證。這些項目不會因 mock 測試通過就標成完成。
