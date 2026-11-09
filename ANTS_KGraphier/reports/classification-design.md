# 固定擷取分類實驗設計

此模組回答「現有子圖是否有可學習的惡意訊號」，不訓練或修改擷取器，也不把 ProvG-Searcher 的距離解釋為惡意機率。入口為 `python -m ants_kgraphier.classification`，與既有 retrieval／segmentation 分開。

## 人工標籤與抽樣

只讀 SQLite `labels`，不讀 selector 的 `weak.jsonl`。`benign` 明確表示正常；`Tdddd`、`Tdddd.ddd` 與其 `_實例後綴` 是可追溯的原始人工 Technique 標籤。完整字串必須符合規則，後綴限英數及連字號。這是本地標籤格式解析，不聲稱已驗證 ID 在某版 ATT&CK catalog 中的存續狀態。`label-map.json` 保留 raw、status、完整 ID、父 Technique、事件數；其他值（包括 null）列入 unknown 稽核。

圖含至少一筆已知惡意事件則 binary=1；全數明確 benign 才為 0；其餘 binary=null。Technique 答案為圖內惡意事件父 Technique 聯集。未知事件存在時，已知 Technique 正例有效，其餘 Technique loss/evaluation 遮罩，不能當成陰性。標籤 sidecar 另存 malicious IDs、逐 Technique 事件、錨點狀態、完整性、來源 SHA-256、事件標籤 hash、抽樣來源。

每錄製的 Registry row 排序後，以 `Random(str(seed)+recording_sha256)` 排出固定抽樣順序，預設 seed=17、每錄製 2,000 錨點。三擷取器與兩個預算共用同一順序及清單。train 僅使用共同均勻錨點，不依標籤增補（舊版實驗曾補入惡意錨點，不能與本版抽樣協定混稱）。validation 整個 split 若任一擷取條件缺少任一 binary 類別，整個共同清單依序擴至 8,000、全部 Registry 錨點；仍不足會保存資料但阻止訓練選模。test 不依結果擴樣。smoke 唯一縮小的是初始每錄製抽樣數與訓練 epochs；validation 擴充規則保留。

所有條件固定 hops=2、fanout=8、offline，預算 33 與 128。window 不必用滿預算。每張原始圖、評估中的大小分組及實際事件總數，保留真實圖大小。既有 `budget_truncated` 同時涵蓋 fanout clipping；不能只把它解釋成超出 budget。TREC 另有詳細 sampling diagnostics。

## 分割與可主張範圍

沿用 `configs/segmentation-splits.json`，已知 APT 共用背景在同一 dependency group。prepare 先對整份 SQLite 做原始事件 SHA-256 跨錄製／分割重複稽核；有跨分割完全相同事件則阻擋準備，需先確認背景來源、合併 group 並重建 splits。這個 hash 含原始時間、UUID 與標籤，不能偵測改名、改時間的重用腳本。已知錄製／group 跨分割另由 loader 拒絕。

結論限於跨錄製的開發驗證；腳本重用尚未確認。既有 pilot test 曾被檢視，不能稱為全新 blind test 或未見腳本泛化。所有來源、共同 anchors、資料內容及模型 hash 都保存；未完成階段保留 `.building`，後續命令拒絕讀取。

## 特徵與模型

沿用 `extract.symbolic` 的 entity–event–entity 與同 actor 的嚴格 PRECEDES 邊；相同時間無先後邊。原始身份僅建立鄰接，不作特徵；時間只建立先後關係，不使用差值。輸入白名單為節點類型、操作、錨點標記、KG ancestor-prefix multihot。操作、類型與可用 prefix 詞彙只由 train 建立；未見操作／類型進 Unknown，未見 prefix 不加特徵。事件也攜帶自己的 Registry prefix context，讓 anchor/no-message 對照能使用相同 KG 證據。

原始事件 ID、row、路徑、程序名稱、錄製來源、timestamp_raw、人工標籤、抽樣類別均不進特徵。KG/no-KG 使用同一詞彙與輸入寬度；no-KG 只把 prefix 區塊歸零。

主模型使用兩層 64 維 R-GCN：三種有向關係各加反向邊，共六個 relation-specific mean aggregation，加 self transform、ReLU、dropout=0.2。事件 mean pooling、max pooling、錨點事件表示串接為 192 維。binary head 為 192→64→1；Technique head 為 192→64→C，各自 sigmoid。C 僅含 train 出現的父 Technique。Batch 使用 disjoint union，沒有 padding 或跨圖邊；每圖 pool 獨立。

對照為 train 類別先驗（binary threshold=0.5 時即多數類別）、僅錨點 MLP、操作／節點特徵計數的線性 logistic/OVR、取消訊息傳遞但保留 pooling 與分類頭的模型、R-GCN KG/no-KG。計數基準透過 BCE 訓練獨立 logistic outputs，無需 sklearn。compare 的 anchor/pool 使用 KG，counts 使用 no-KG；所有條件使用同一樣本及標籤。

## 損失、選模、續訓

binary 與 Technique masked BCE 各取平均後相加。每輸出正類權重只用 train 已知標籤計算 negative/positive，最大 20。AdamW lr=0.001、weight_decay=0.0001，batch=32，最多 50 epochs，patience=8，seeds=7/17/27。訓練從頭開始，不需要預訓練。

每 epoch 僅在 validation 分別選 binary 與共用 Technique threshold（0.05–0.95，每格 0.05）。同分優先接近 0.5，其次較小值。checkpoint score 是 binary balanced accuracy 與有正例支持的 oracle Technique macro-F1 平均；無可評估 Technique 時僅用 binary 並標記不足。保存最佳模型及其門檻，test 只在凍結後評估。

`last.pt` 保存當前／最佳權重、optimizer、epoch、patience、history、Python/Torch/CUDA RNG。resume 要求相同資料 hash、程式 hash、Torch 版本、裝置及訓練設定，僅允許延長總 epochs；必須使用新的 output。已觸發 early stopping 的 run 不會因 resume 重新清空 patience。CPU 續訓一致性有回歸測試；GPU 路徑尚未於本機驗證，要求 deterministic operations，無法保證的 backend 會報錯。

目前資料與編碼載入記憶體，適用本地 bounded corpus；不是 TB 級串流訓練器。

## 指標與產物

binary 主指標為 (TPR+TNR)/2；任一類別缺失時為 null，另列 precision/recall/F1、兩類 macro-F1、PR-AUC（以同分群組計算 average precision）、混淆矩陣及陽性比例。對類別平均與對有效錄製平均分開命名，後者揭露有效錄製數。

Technique 同時報已知惡意子圖 oracle 與 binary gate 後端到端的 micro/macro-F1、逐類支持數及 precision/recall/F1。macro-F1 明示只平均觀測到正例的類別；逐類結果仍列出所有 train 類別。balanced accuracy 只平均同時有正負樣本的類別並揭露有效類別數。train 未見類別另列 graph 數及去重事件數，絕不改為 benign。

分組包含錨點狀態、各錄製、各 Technique、截斷狀態與實際事件數區間；另在相同事件集合僅留第一圖後重算指標，揭露原始／去重統計。這不等於消除所有重疊樣本或建立獨立置信區間。binary 與 Technique 錯誤案例各保留至多 100 圖供追溯。

prepare 交付 manifest、label-map、split-audit、共同 anchors 及六套 graphs/labels；train 交付 model.json、best/last.pt 與 hash；predict 交付逐圖 binary/Technique 機率與 oracle/gated 預測；evaluate 交付完整 test 指標與分組；compare 交付逐 run JSON/Markdown 比較表。需要研究結論時必須完成預設 50-epoch 上限、三 seeds，檢查模型是否穩定超過 anchor/counts；smoke 結果不構成效益驗收。
