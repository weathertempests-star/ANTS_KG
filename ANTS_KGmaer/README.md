# ANTS_KGmaer

Registry 功能知識支援的逐事件判別研究程式。DGX Spark 只提供模型推論 API；此專案在內網研究機器執行資料處理、KG 工具、agent、對照實驗與評分。

**目前為持續實作中的版本，尚未完成整個研究流程。** 實際進度與剩餘驗收見 [實作追蹤](docs/IMPLEMENTATION_STATUS.md)。不將合成測試或模擬模型結果宣稱為真實惡意偵測成效。

Spark client 安裝、實際模型設定與次要動態歷史實驗見 [SLM client 指引](docs/SLM_CLIENT.md)。

## 程式分層

```text
ANTS_KGmaer/
  ants_kgmaer/
    common/        穩定序列化、雜湊與輸出管理
    data/          來源驗證、串流匯入、適配、匿名化、分組、抽樣、上下文
    knowledge/     分拆保留的已驗證知識核心、唯讀查詢與快取
    models/        Spark HTTP／tokenizer／模型介面
    agent/         證據、工具與受限流程
    experiments/   實驗設定、runner與resume
    evaluation/   獨立答案關聯與統計
    presentation/  本機報告與案例展示
    resources/     凍結的197節點KG snapshot
  configs/         11份錄製清單、人工標籤映射與Registry欄位契約
  tests/           unittest回歸與整合測試
  docs/            研究契約與驗收紀錄
```

各模組只負責一個環節；CLI 負責參數與命令註冊。原有知識演算法拆成 paths／schema／engine，來源雜湊保存在 [provenance](docs/upstream-provenance.json)。不修改上一版 `AGENTS.md`、原始資料或既有 vault。

## 已可執行的資料流程

從本目錄執行，Python 3.10+；資料層不需要第三方套件：

```bash
python -m ants_kgmaer --help
python -m unittest discover -s tests -v
python -m ants_kgmaer ingest \
  --sources configs/sources.json --data-root ../data \
  --labels configs/labels.json --relations configs/relations.json \
  --output workspaces/recordings-v1
python -m ants_kgmaer select \
  --dataset workspaces/recordings-v1 \
  --negative-cap 2000 --output workspaces/pilot-v1
```

輸出目錄必須全新，避免覆蓋既有研究產物。中斷的匯入標記為 incomplete，不可拿去評估；完整來源會驗證 SHA-256 與逐檔筆數。大檔 JSONL 及 CHT JSON array 都採串流解析。

`events.sqlite` 與 `answers.sqlite` 分開儲存。EventStore 只開前者；模型可見資料再由白名單重新組成，不傳來源檔名、label、timestamp_raw、來源 UUID 或完整 state。抽樣機率僅留給 evaluator，不能傳給模型。

目前未收到 value encoding 的匯出規格，因此 value 操作預設 `boundary_status=unresolved`。若確認某錄製有獨立 ValueName 欄位或特定串接方式，請在 `configs/relations.json` 的 recording_overrides 記錄規格與 evidence，重新建立資料版本。不得只因模型更大就猜測欄位語意。

主評估的 default split 是固定模型的 retrospective evaluation，不宣稱盲測。自訂分組需涵蓋每份錄製，且不能將已知／新發現依賴群組拆到不同 split。

## 執行、評分與本機報告

下列流程已可執行。範例使用 mock、只取前 20 個抽樣目標，驗證工程流程；不代表模型成效，也不代表所有錄製的覆蓋。Mock 固定拒答，token 數也是合成估計。

```bash
python -m ants_kgmaer run \
  --config configs/mock-engineering.json \
  --dataset workspaces/recordings-v1 --selection workspaces/pilot-v1 \
  --output runs/mock-engineering-v1
python -m ants_kgmaer evaluate \
  --dataset workspaces/recordings-v1 --selection workspaces/pilot-v1 \
  --run runs/mock-engineering-v1 --output runs/mock-engineering-v1-evaluation
python -m ants_kgmaer report \
  --evaluation runs/mock-engineering-v1-evaluation \
  --run runs/mock-engineering-v1 --output runs/mock-engineering-v1-report
```

用瀏覽器開啟 `runs/mock-engineering-v1-report/report.html`。報告不載入外部資源，log 文字會跳脫 HTML；各 TP/TN/FP/FN/未決類別只展示實際存在的前幾筆，不編造案例。報告與評分目錄必須全新。

`run` 保存凍結設定、SQLite checkpoint、predictions、實際送出的 evidence packets、prompts、tool calls、usage 與校驗 manifest。使用完全相同設定及程式版本可恢復中斷執行；已送出而未收到回應的請求保留未知用量上界。已完成目錄不再推論或改寫，產物遭手動修改時拒絕覆蓋。程式／模型／輸入版本改變需另建 run 目錄。

`evaluate` 是獨立開啟人工答案庫的階段。BA_all 是兩類各自正確比例的平均；缺失、失敗和拒答保留在分母。輸出包含逆抽樣機率加權與未加權結果、2×3 混淆表、逐錄製／cohort／依賴群組／split 統計及逐事件評分。單類資料的 BA 與 macro-F1 為 null。沒有完成 manifest 的中斷 run 也可評分，會明示 run_complete=false；這不代表該 run 已完成工程驗收。

目前條件為 `raw`、`normalized`、`text`、`graph`、`flat`、`unrelated`、`agent`、`budget`、`replay`。複製範例設定並修改 condition，每組使用獨立輸出目錄。`flat` 保留相同完整事實，以文字序列表示，不能當作移除關係知識的對照。`unrelated` 使用相同證據上限，但不保證實際 token 數完全相同。

Replay 設定須指定 `"condition": "replay"` 和 `"replay_run": "../runs/source-agent"`；相對路徑從設定檔目錄解析。來源必須是完整 agent run，資料、模型、歷史與預算須相同。Replay 使用來源最後交付的證據和工具觀察，若需要再裁減證據會拒絕執行；來源未形成最終證據封包時記為未決，不丟棄該事件。預測內 `replay.acquisition_usage` 單列取得證據成本，`usage` 是 replay 自己的成本，不能將取得的證據當成免費。

兩組完成評分後可執行：

```bash
python -m ants_kgmaer compare --left runs/left-evaluation \
  --right runs/right-evaluation --output runs/comparison.json
```

比較器先逐事件確認目標、答案、抽樣權重、split 與依賴群組相同，再做成對依賴群組 bootstrap。輸出差值方向為 right−left；依賴群組少時區間不穩定，不能以大量事件數掩蓋此限制。

覆蓋分析 `prepare`、重複群組敏感度 `duplicates`、人工主張審核 `review-export`／`review-import` 已接通；操作與限制見 [分析工作流程](docs/ANALYSIS_WORKFLOW.md)。新評分另輸出 `per_recording.csv`、`confusion_matrices.csv` 與包含所有 FP/FN/未決事件的 `error_cases.jsonl`。

`coverage-population --dataset ... --output ...` 分析完整 Registry 母體而不呼叫模型；`export-data --dataset ... --output ...` 串流匯出 `events.jsonl` 與 `annotation_audit.csv`。`verify <directory>` 核對必要產物的 checksum 與凍結設定。較早產物若未校驗所有必要檔案會明示拒絕，不補寫假校驗或覆蓋既有 manifest。新報告另提供 `EXPERIMENT_REPORT.md` 與 `per_recording_ba.svg`；新 compare 會在 JSON 旁輸出同名 CSV，保存逐錄製 paired deltas。

Spark 連線介面已實作，但目前沒有實機端點驗收；環境禁止 socket，兩項 loopback HTTP 測試會明示 skip。LangGraph 選用後端也尚未完成安裝與 runtime 驗證，工程測試採 native 有界流程。完整母體 KG 覆蓋實測已完成；整份研究驗收仍在核對，詳見追蹤文件。
