# 研究實作與完成驗收追蹤

本表不是完成宣告。目標是實作整份研究計畫，原始資料、現有197節點知識與Spark推論／Client工具分工不變。

| 要求 | 目前狀態 | 驗收依據／待補 |
|---|---|---|
| 根目錄ANTS_KGmaer、模組清楚 | 已建立 | common/data/knowledge/models/agent/experiments/evaluation/presentation 分層 |
| 11份來源白名單、hash、串流解析 | 已實作；真實全量完成 | source_manifest complete=true；3,721,213事件／2,892,462 Registry／728惡意；來源及DB雜湊驗證 |
| 逐事件人工答案隔離、未知隔離 | 已實作 | events／answers分庫、label白名單與quarantine |
| key/value契約與匿名化 | 已實作保守預設 | value encoding未確認時明示unresolved；仍需實際匯出規格確認 |
| 嚴格先前同程序、同序不推定先後 | 已實作 | 同timestamp及跨錄製限制測試 |
| exact／normalized重疊與依賴群組 | 已實作 | overlap模組；全量audit保存於workspaces/pilot-v1；22,330個pilot目標 |
| 分組split、全量／pilot抽樣與機率 | 已實作 | select CLI與依賴分組／抽樣測試 |
| 197節點／192邊／Session Manager 5節點 | 已驗證 | 凍結snapshot；原演算法分模組後回歸測試 |
| exact/template/ancestor/unknown、邊界不確定 | 已實作 | prepare已輸出22,330個pilot目標的contexts/cache/coverage；完整母體2,892,462事件／158,565查詢已完成，5個產物hash與資料庫筆數通過核對 |
| 唯讀工具、ID白名單、整個主張截斷 | 已實作 | tools/evidence與dynamic_history測試；批次可見ID凍結，動態歷史僅次要agent/replay條件 |
| Spark LAN HTTP與精確tokenization介面 | 已實作介面 | transport模擬測試；尚無使用者實際API端點 |
| LangGraph狀態機、預算、修復與終止 | native已實作測試；LangGraph待runtime驗證 | 非法工具、超額、拒答、失敗不默認benign；LangGraph依賴安裝因網路DNS失敗 |
| A/B/C/D/E/D-flat及agent/replay/budget | 已實作 | 九條件；replay同封包與取得證據成本測試；flat是表示形式對照 |
| 可恢復runner、checkpoint、完整attempt成本 | 已實作，需續查中斷邊界 | 已完成不重複；未知usage留存；已收到回覆重驗；修復額度跨resume不重置；更全面故障注入仍待補 |
| BA_all、macro-F1、FPR、coverage、單類N/A | 已實作 | evaluate CLI；含失敗／拒答／缺失的2×3表、逆抽樣機率加權與分母守恆測試 |
| 逐錄製／命中分層、paired block分析 | 部分完成 | 逐錄製/cohort/split/group與成對依賴群組bootstrap已接上；--prepared加入match/boundary分層 |
| 重複群組等權敏感度、引用人工審核 | 已實作測試 | observed-group等權、衝突labels不合併；review-export/import分開引用有效率與人工支持率 |
| 所有P0–P6／F0–F5產物與HTML案例展示 | 部分完成 | 已實作全部命名產物匯出，包括events.jsonl/annotation_audit.csv/paired CSV/Markdown/SVG；母體作業已驗證；最終規格審核進行中 |
| 端到端離線整合與真實來源處理驗證 | 部分完成 | 真實資料200筆mock與22,330筆prepare已執行；HTTP測試已加入但socket權限拒絕，明示skip；Spark端點待驗證 |
| 最終CLI、安裝、README與完整驗收 | 待完成 | CLI/README/client指引已更新；離線wheel建置與隔離目錄安裝/KG載入成功；最新wheel已重建並隔離安裝，內附KG/renderer與程式hash核對成功；安裝版同樣58通過、5項測試skip（2 HTTP、3 LangGraph）；剩實際HTTP/Spark及LangGraph runtime驗收 |

已完成的全量匯入輸出：`workspaces/recordings-v1`。只有 `source_manifest.json` 的 complete=true 且檔案hash／筆數核對通過才算完成。後續不能因已有部分測試通過而將全目標標為完成。

最近驗證：63項測試執行，58通過、5項跳過（2項loopback HTTP因環境禁止socket、3項LangGraph因依賴不可用）；舊版保留74項測試通過。跳過不代表實機驗收完成。新增功能操作見[分析工作流程](ANALYSIS_WORKFLOW.md)，外部驗收步驟見[整合驗收](INTEGRATION_ACCEPTANCE.md)。

本輪檢查紀錄：[VERIFICATION_RECEIPT.json](VERIFICATION_RECEIPT.json)。完整母體：ancestor 1,599,620、boundary_unresolved 1,116,072、exact 156,610、unknown 20,160；惡意子集705筆邊界未確認。

最新檢查紀錄：[VERIFICATION_RECEIPT_V2.json](VERIFICATION_RECEIPT_V2.json)。目前可執行的本地檢查已完成；後續整合驗收需要可建立socket、可安裝LangGraph的環境，以及實際Spark部署資料，整體目標尚未達成。
