# ANTS_KGraphier 研究進度

更新日期：2026-11-09。開發分支：`ANTS_KGraphier`。

## 研究目標

研究 Registry 事件中心的可追溯子圖擷取、分析檢索、學習式事件選擇及圖分類。區分分析相關性、結構 containment 與惡意分類，分開報告 CHT/APT 與 SAGA 實驗。

## 目前狀態

下列文件位於 `ANTS_KGraphier` 分支；在 `ANTS_KGmaer` 分支可能無法開啟。依 [README](../../ANTS_KGraphier/README.md)、[分類驗證](../../ANTS_KGraphier/reports/classification-validation.md) 與 [SAGA 驗證](../../ANTS_KGraphier/reports/saga-validation.md) 整理，未重新驗證其中結果。

| 項目 | 狀態 | 依據／限制 |
|---|---|---|
| 事件索引、window／temporal 擷取與來源追溯 | 已實作，有既有驗證報告 | 大型索引與原始資料本機保留 |
| ProvG-Searcher backbone、檢索與分析展示 | 已實作 | containment 工程驗證不等同人工相關性評估 |
| 學習式切圖 selector | 已實作 | 需與檢索模型分開紀錄 checkpoint 與監督設定 |
| CHT/APT 分類比較 | 已完成既有短訓練試跑 | 報告記錄 108 runs、兩 epochs；正式完整訓練待完成 |
| SAGA v2 格式與標籤稽核 | 已完成既有掃描 | 報告記錄 38 份錄製；來源 checksum 保留於設定／本機報告 |
| SAGA 三錄製機制試跑 | 已完成既有試跑 | 報告記錄 54 runs；test 僅 30 圖，不足以支持模型優勢 |
| 完整 SAGA 正式比較 | 受來源證據阻擋 | M1–M10 組成與背景依賴映射不足，不能任意隨機切圖替代 |

## 下一步

- [ ] 補足 SAGA M1–M10 的來源組成、模板／背景映射證據。
- [ ] 建立完整依賴分組與跨 split 重複片段稽核。
- [ ] 凍結正式錨點清單、budget、模型與 seed 設定。
- [ ] 來源條件成立後執行正式 2,000 錨點、budget 33/128、最多 50 epochs、三 seeds 比較。
- [ ] 補足 Technique 測試支持與來源群組層級的不確定性分析。
- [ ] 若主張分析檢索品質，建立獨立人工相關性標註。

## 進度紀錄

| 日期 | 工作／實驗 | 版本與產物 | 結果與限制 |
|---|---|---|---|
| 2026-11-09 | 建立獨立分支與進度入口 | 共同歷史基準 `be5fefc`；KGraphier 初始程式由本次分支提交保存 | 現有試跑結果依文件盤點，未重跑實驗 |

後續每列補上程式 commit、資料／KG hash、模型／上游版本、設定／seed 與本機產物位置。詳細 JSON、逐圖預測與事件 trace 留在本機；Git 保存 Markdown 摘要及重現設定。
