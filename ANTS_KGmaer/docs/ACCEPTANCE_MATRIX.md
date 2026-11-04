# 研究計畫驗收對照

本表按原 `REGISTRY_EXPERIMENT_PLAN.md` 的 P0–P6 與 `SLM_AGENT_FRAMEWORK_PLAN.md` 的 F0–F5 核對。它列出目前可檢驗的實作證據與未驗證範圍，不代表全部完成。

| 階段 | 程式與命令 | 已有驗證 | 尚未證明的範圍 |
|---|---|---|---|
| P0 資料契約 | data/sources、ingest、contracts；`ingest` | 11來源雜湊、全量3,721,213筆匯入；fixture未知標籤隔離 | key/value匯出規格仍未提供，保守unresolved是預設 |
| P1 適配 | normalize、redaction、export；`export-data` | event/answer分庫；白名單context；events.jsonl與annotation_audit.csv匯出測試 | 未將所有平台識別形式視為已完備匿名化；新格式須另審 |
| P2 切分與上下文 | overlap、sampling、context；`select`、`prepare` | exact重疊依賴群組、抽樣機率、同序不可推先後；22,330 pilot封包 | VM／背景腳本共同來源依賴仍可能超出已知群組 |
| P3 KG 表達 | repository、evidence、preparation、population | 197節點／192階層邊／46語意邊；Session Manager5節點；pilot完整覆蓋產物 | 全母體2,892,462事件與158,565查詢已完成並核對5個產物hash；保留未知及邊界不確定 |
| P4 runner | config、runner、journal、session | 九條件；200筆真實來源mock；中斷成本、回覆重驗、修復次數、hash驗證 | 真實SLM未提供端點；HTTP socket測試受環境限制；LangGraph未runtime驗證 |
| P5 評分 | scoring、comparison、duplicates、review | 含拒答／缺失分母、加權、單類N/A、逐錄製／technique／coverage；paired與衝突labels測試 | 真實模型品質、完整人工審核尚無結果；群組敏感度僅觀測抽樣群組 |
| P6 呈現 | presentation/report、discussion | HTML、EXPERIMENT_REPORT.md、獨立SVG；跳脫log、無案例不捏造 | 未以真實模型產生TP/FP/FN；工程報告不支持偵測效益主張 |
| F0 | P0–P3 | 個別資料與檢索測試；真實pilot覆蓋 | 全母體作業完成；key/value規格未知仍明示不確定 |
| F1 | ToolBox、schemas、fixed_evidence | lookup_registry、expand_knowledge、次要get_prior_context；唯讀與ID白名單 | 不把動態歷史政策和固定K主實驗混為一組 |
| F2 | AgentSession、graph、VllmAdapter | bounded native、格式修復、引用驗證、預算；transport替代測試 | LangGraph安裝與真實HTTP／Spark仍待驗收 |
| F3 | mock-engineering-200設定、usage.json | 200筆全部有結果，11個產物hash通過verify | mock token與延遲不能估算真實服務容量 |
| F4 | run/evaluate/compare/replay | 同目標逐列join；同取得證據replay及取得成本；九條件fixture | 實際模型配對效果尚無量測 |
| F5 | report、review-export/import | 工程案例展示及盲化主張審核流程 | 人類支持率須真正完成審核；無主張／待審是N/A或pending |

命名產物對照：SQLite 是主要事件與答案儲存；`export-data` 提供原計畫的 `events.jsonl`／`annotation_audit.csv`。`prepare` 提供 contexts/cache/coverage。Runner 提供 predictions、usage.json與逐事件usage.jsonl、schemas、prompts、tool_calls、checkpoint。Evaluator 提供 metrics、per_recording、confusion_matrices、error_cases。Compare 在指定JSON旁提供同名CSV的逐錄製paired deltas。Report提供HTML、Markdown與SVG。

最終仍須核對：對使用者實際服務的驗收邊界，以及任何仍未覆蓋的計畫要求。不能因表內多數欄位已有測試就將整個目標標記完成。
