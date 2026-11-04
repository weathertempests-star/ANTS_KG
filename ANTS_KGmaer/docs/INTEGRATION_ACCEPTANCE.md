# 尚待執行的整合驗收

本機核心、完整資料覆蓋與 mock 流程已驗證。以下項目需要本環境沒有的能力，尚未以實測證明；不能將 skip 當成通過。

## A. 允許 socket 並已安裝 LangGraph 的研究機器

從 `ANTS_KGmaer` 根目錄執行：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install '.[agent]'
.venv/bin/python -m unittest discover -s tests -v
```

目前共 63 項測試。這個環境的結果是 58 通過、5 跳過：2 項 loopback HTTP 被 socket 權限限制、3 項 LangGraph 因依賴不存在而跳過。在具備上述能力的機器上，這 5 項必須實際執行；若仍有 skip，先保留原因，不宣稱已完成此 gate。

需要保存的證據：完整 unittest 結果、Python 版本、`pip freeze`。這些測試使用合成模型回覆與臨時 fixture，不需要連接 Spark，也不向外傳送原始 log。它們驗證：

- 真正經過 HTTP 的認證、tokenize、模型回覆與 503 失敗成本。
- native 與 LangGraph 在同一狀態／預算下的結果一致。
- 恢復兩輪檢索後或已 finalize 時，LangGraph 不再多做一輪檢索。

## B. 真實 Spark 服務

依 [SLM client 指引](SLM_CLIENT.md) 建立實際設定，提供內網 origin、model alias、repo、權重與 tokenizer commit、container digest、精度。API key 留在研究機器的環境變數／key file，不寫入設定或驗收回覆。

先核對服務提供 `/health`、`/v1/models`、`/tokenize`、`/v1/chat/completions`，並確認部署記錄與設定身分一致；API alias 本身不能證明權重版本。再以有 `engineering_limit=200` 的設定執行新 run 目錄，保存：

- `manifest.json` 與 `verify` 結果。
- `preflight.json`、`config.json`、`usage.json`。
- tokenization／格式／引用驗證錯誤與 model-call 的 p50/p95。
- 明示模型版本、精度、上下文與並行設定。

200 筆工程驗收不證明模型有偵測能力，也不取代固定資料與設定後的正式配對消融。key/value 邊界未確認時仍採 unresolved，不能為了提高覆蓋率猜測欄位。

## 回報範圍

可回報測試成功／失敗／skip 摘要及去除機密的部署身分，不需貼 API key、完整原始 log 或私有事件內容。只有得到實際執行證據後，才能把對應驗收項目標成完成。
