# 分類流程本地驗證

本次新增獨立 `ants_kgraphier.classification`，提供 prepare、audit、train、predict、evaluate、compare。既有 extractor、selector、retrieval 程式沒有修改。架構與標籤政策見 [設計文件](classification-design.md)。

## 工程驗證

- `python -m unittest discover -s ANTS_KGraphier/tests -v`：29 項通過，包含 8 項分類測試。涵蓋多 Technique、unknown 遮罩、未見類別、全陰性 validation 拒絕選模、共同錨點及擴樣、跨分割重複、特徵隔離、無邊圖、批次一致性、所有模型輸出形狀、無 Technique 類別、完整 compare 命令產物、續訓與手算指標。
- CPU 兩 epoch 不間斷訓練與一 epoch 加 resume：逐 tensor 完全相同，history 相同，推論成功。
- 六個擷取條件的完整共同錨點集合、graphs/labels SHA-256：一致。
- seed=17，每條件每 split 抽五圖，共 90 圖：從 SQLite 重新擷取與人工標籤 sidecar 核對，全數一致。見 [資料驗證 JSON](classification-data-verification.json)。
- Python compileall 通過；未變更既有標準化、檢索與 selector 的公開介面。

測試輸出見 [classification-tests.log](classification-tests.log)，套件版本見 [classification-environment.txt](classification-environment.txt)。環境檔的 editable Git commit 不包含未提交變更；每個模型另外記錄分類程式與資料 SHA-256，不能只用 pip freeze 還原本次程式。

## 真實本地資料

資料來源是既有六份 CHT、五份 APT SQLite，沿用 recording/dependency-group 分割。共辨識 29 種原始人工標籤（含 benign），格式未知標籤 0；跨分割完全相同原始事件 0。這種原始 hash 檢查不能排除改變 UUID／時間的共用腳本。

本地 smoke 初始每錄製 30 個共同 Registry 錨點，train 增補既有惡意 Registry 錨點；validation 因初始全陰性，依預先固定順序擴至 8,000。每條件共 8,876 張圖：726 train、8,000 validation、150 test。test 清單未依分類結果擴充。

| 條件 | validation 陽性 | validation 陰性 | test 陽性 |
|---|---:|---:|---:|
| temporal-33 | 20 | 7,980 | 8 |
| temporal-128 | 29 | 7,971 | 8 |
| trec-33 | 21 | 7,979 | 8 |
| trec-128 | 30 | 7,970 | 8 |
| window-33 | 6 | 7,994 | 8 |
| window-128 | 6 | 7,994 | 8 |

這種支持數足以執行 binary 選模，但不代表門檻穩定或 validation 代表部署分布。許多 test Technique 在 train 未出現；各條件的已知／未覆蓋支持與去重事件數均另列，沒有改為 benign。

## 實驗範圍

本地矩陣使用三擷取器、budget 33/128、六種模型/KG 條件、seeds 7/17/27，短訓練上限兩 epochs。108 runs 全部完成，最佳 checkpoint、逐圖機率及 test 指標均已保存。比較與逐類支持彙整於 [本地比較表](classification-local.md) 及 [完整摘要 JSON](classification-local.json)。

短訓練結果沒有支持 R-GCN 在所有條件穩定勝過基準。temporal-128 的 KG R-GCN binary balanced accuracy 為 0.7676 ± 0.1163，高於 counts 的 0.5505 ± 0.0665；但 temporal-33 的 KG R-GCN 為 0.5669，低於 counts 的 0.6127，window 的 KG R-GCN 為 0.4953，低於 counts 的 0.6450。這些是三 seeds 的平均及 population standard deviation，並非信賴區間或收斂後比較；KG 效果亦隨條件改變。

R-GCN 在這份 test 的已知 Technique oracle macro-F1 均為 0。所有條件只有 T1071 有一張已知類別陽性；T1005、T1016、T1059、T1548 未被 train 類別字典覆蓋。沒有足夠支持評估多數 train Technique。錯誤案例例如 temporal-128/KG/seed7 的圖 `522908c80fd363a449bdf91b3545946219298083325c3349b0439b046634767d`：真值 T1016，預測 T1219；T1016 本就不在輸出字典，這不能視為模型具備未知類別辨識能力。

window 的實際圖大小最多 17 事件，預算 33/128 因此產生相同事件集合與相同模型結果；不能將這一組「無差異」解讀為 budget 通常沒有影響。其他條件有更大的實際圖及不同截斷情形，完整統計見比較表。

完整研究預設（每錄製初始 2,000 錨點、最多 50 epochs、patience=8）尚未執行。本次驗證工程可執行性，不將兩 epochs 的分數當成收斂後模型比較；研究驗收仍需完整訓練及更充分的 Technique test 支持。README 提供完整遠端命令。

產物位於 `artifacts/classification-smoke-v1/` 與 `artifacts/classification-smoke-runs-v2/`。早期 `classification-smoke-runs-v1` 因重複編碼成本中斷，保留 `.building`，不屬於有效結果。沒有刪除標記後將它冒充完成快取。
