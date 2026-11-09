# 本地固定擷取分類驗證

初始每錄製 30 個共同錨點，完成 54 runs；實際訓練 epochs 為 [2]。
這是跨錄製開發 smoke，不是完整 2,000 錨點／最多 50 epochs 的研究驗收，也不支持未見腳本泛化。

原始標籤格式未知數：0；跨分割完全相同原始事件：0。hash 稽核不能排除改名或改時間的腳本重用。

## 資料支持與圖大小

| 條件 | Split | 圖數 | 陽性 | 去重事件集合 | 去重陽性 | 平均事件數 | 最小–最大 |
|---|---|---:|---:|---:|---:|---:|---|
| temporal-33 | validation | 8000 | 102 | 7999 | 101 | 32.75 | 1–33 |
| temporal-33 | test | 30 | 2 | 30 | 2 | 30.37 | 1–33 |
| temporal-33 | train | 30 | 6 | 30 | 6 | 31.90 | 20–33 |
| trec-33 | validation | 8000 | 136 | 7999 | 135 | 32.80 | 1–33 |
| trec-33 | test | 30 | 2 | 30 | 2 | 30.37 | 1–33 |
| trec-33 | train | 30 | 6 | 30 | 6 | 33.00 | 33–33 |
| window-33 | validation | 8000 | 85 | 8000 | 85 | 14.92 | 1–17 |
| window-33 | test | 30 | 2 | 30 | 2 | 13.33 | 1–17 |
| window-33 | train | 30 | 5 | 30 | 5 | 14.23 | 2–17 |

## 三 seeds 比較

以下為 graph-level binary balanced accuracy 的平均 ± population standard deviation；不是對錄製平均，也不是信賴區間。Technique macro-F1 只含 test 具有正例支持的 train 類別。

| 條件 | 模型 | KG | Seeds | Binary BA | Oracle Technique macro-F1 | E2E Technique micro-F1 |
|---|---|---|---|---|---|---|
| temporal-33 | anchor | True | [7, 17, 27] | 0.5000 ± 0.0000 | 不可評估 | 0.0000 ± 0.0000 |
| temporal-33 | counts | False | [7, 17, 27] | 0.5655 ± 0.1094 | 不可評估 | 0.0000 ± 0.0000 |
| temporal-33 | pool | True | [7, 17, 27] | 0.5000 ± 0.0000 | 不可評估 | 0.0000 ± 0.0000 |
| temporal-33 | prior | False | [7, 17, 27] | 0.5000 ± 0.0000 | 不可評估 | 0.0000 ± 0.0000 |
| temporal-33 | rgcn | False | [7, 17, 27] | 0.6905 ± 0.1606 | 不可評估 | 0.0000 ± 0.0000 |
| temporal-33 | rgcn | True | [7, 17, 27] | 0.5536 ± 0.1436 | 不可評估 | 0.0000 ± 0.0000 |
| trec-33 | anchor | True | [7, 17, 27] | 0.5000 ± 0.0000 | 不可評估 | 0.0000 ± 0.0000 |
| trec-33 | counts | False | [7, 17, 27] | 0.4643 ± 0.1010 | 不可評估 | 0.0000 ± 0.0000 |
| trec-33 | pool | True | [7, 17, 27] | 0.5000 ± 0.0000 | 不可評估 | 0.0000 ± 0.0000 |
| trec-33 | prior | False | [7, 17, 27] | 0.5000 ± 0.0000 | 不可評估 | 0.0000 ± 0.0000 |
| trec-33 | rgcn | False | [7, 17, 27] | 0.5595 ± 0.0607 | 不可評估 | 0.0000 ± 0.0000 |
| trec-33 | rgcn | True | [7, 17, 27] | 0.6071 ± 0.1051 | 不可評估 | 0.0000 ± 0.0000 |
| window-33 | anchor | True | [7, 17, 27] | 0.5476 ± 0.0673 | 不可評估 | 0.0000 ± 0.0000 |
| window-33 | counts | False | [7, 17, 27] | 0.4107 ± 0.0000 | 不可評估 | 0.0000 ± 0.0000 |
| window-33 | pool | True | [7, 17, 27] | 0.5536 ± 0.1296 | 不可評估 | 0.0000 ± 0.0000 |
| window-33 | prior | False | [7, 17, 27] | 0.5000 ± 0.0000 | 不可評估 | 0.0000 ± 0.0000 |
| window-33 | rgcn | False | [7, 17, 27] | 0.5000 ± 0.0000 | 不可評估 | 0.0000 ± 0.0000 |
| window-33 | rgcn | True | [7, 17, 27] | 0.5417 ± 0.0589 | 不可評估 | 0.0000 ± 0.0000 |

## 未覆蓋 Technique 與限制

- temporal-33：test 已知類別支持 `{"T1003": 0, "T1083": 0}`；未覆蓋 `{"T1005": {"graphs": 1, "events": 1}, "T1059": {"graphs": 1, "events": 2}}`。
- trec-33：test 已知類別支持 `{"T1003": 0, "T1083": 0}`；未覆蓋 `{"T1005": {"graphs": 1, "events": 1}, "T1059": {"graphs": 1, "events": 2}}`。
- window-33：test 已知類別支持 `{"T1083": 0}`；未覆蓋 `{"T1005": {"graphs": 1, "events": 1}, "T1059": {"graphs": 1, "events": 1}}`。

validation 由固定順序擴充，不增補惡意錨點；test 清單固定。目前 train 同樣只採均勻錨點，不依惡意標籤增補；來源不同仍可能造成先驗差異。
短訓練及 test 支持不足限制了這張表的解讀；即使某次 GNN 分數較高，仍需完整訓練、跨 seed 穩定性與獨立資料才能作效益結論。
逐類 precision/recall/F1、完整混淆矩陣、各錄製與去重分組、未覆蓋事件數、binary/Technique 錯誤案例在每 run 的 test.json；逐圖機率與 gate 後預測在 predictions.jsonl。

完整本地產物：`ANTS_KGraphier/artifacts/saga-v2/pilot-prepared`、`ANTS_KGraphier/artifacts/saga-v2/pilot-runs`。
