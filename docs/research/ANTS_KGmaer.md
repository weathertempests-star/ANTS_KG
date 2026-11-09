# ANTS_KGmaer 研究進度

更新日期：2026-11-09。開發分支：`ANTS_KGmaer`。

## 研究目標

以 Registry 功能知識與受限 SLM agent 支援逐事件判別，比較 raw、normalized、text、graph、flat、unrelated、agent、budget、replay 等條件，分別評估效果、證據與成本。

## 目前狀態

依 [實作追蹤](../../ANTS_KGmaer/docs/IMPLEMENTATION_STATUS.md) 與 [README](../../ANTS_KGmaer/README.md) 整理；尚未完成真實模型的整體研究驗收。

| 項目 | 狀態 | 依據／限制 |
|---|---|---|
| 資料匯入、答案隔離、依賴分組、抽樣 | 已實作並有既有全量紀錄 | 既有追蹤記錄 11 份來源、3,721,213 事件；原始資料不進 Git |
| KG snapshot 與唯讀工具 | 已實作 | 197 節點；完整母體覆蓋分析有既有紀錄 |
| runner、resume、評分、成對比較與報告 | 已實作，部分驗收待完成 | mock 驗證工程流程，不代表偵測成效 |
| Spark HTTP／tokenization | 介面已實作 | 實際端點與實機整合待驗證 |
| LangGraph | 待 runtime 驗證 | native 流程已有測試；不能視為 LangGraph 實機通過 |
| 真實模型條件比較與研究結論 | 待完成 | 需固定模型、設定、資料版本及成本紀錄 |

## 下一步

- [ ] 確認 value encoding／key-value 邊界的匯出規格與證據。
- [ ] 完成 Spark 實際 HTTP 端點與 tokenizer 驗收。
- [ ] 在可用環境驗證 LangGraph runtime。
- [ ] 完成 runner 中斷邊界與必要故障注入驗收。
- [ ] 凍結正式比較設定，執行真實模型與各對照條件。
- [ ] 完成人工引用審核、依賴群組統計與最終研究報告。

## 進度紀錄

| 日期 | 工作／實驗 | 版本與產物 | 結果與限制 |
|---|---|---|---|
| 2026-11-09 | 建立獨立分支與進度入口 | 共同歷史基準 `be5fefc`；設定見本次管理提交 | 依既有文件盤點，未重跑實驗 |

後續每列補上程式 commit、資料／KG hash、模型版本、設定／seed 與本機 run 路徑；只提交摘要，不提交原始事件、權重與完整 evidence packets。
