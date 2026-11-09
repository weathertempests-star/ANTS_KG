# 實作與驗收紀錄

日期：2026-11-03。範圍：可追溯 Registry 事件中心擷取、ProvG-Searcher backbone、現有資料上的研究驗證。沒有將功能匹配改成惡意分類。

## 已完成與證據

| 要求 | 實作／驗證 | 證據 |
|---|---|---|
| 實作置於 ANTS_KGraphier | 獨立套件、CLI、configs、scripts、tests、reports、artifacts | [README](../README.md) |
| 現有資料驗證 | 六份 CHT＋五份 APT 全部 hash 與筆數核對；串流匯入 3,721,213 筆事件，含 2,892,462 筆 Registry | [完整來源 manifest](../artifacts/events.manifest.json) |
| 可追溯事件中心擷取 | source SHA-256＋零起算事件序號；保留原始事件 hash、擴展 parent／endpoint／方向／hop | [extract.py](../ants_kgraphier/extract.py) |
| 時序與預算 | offline／past；同值不建順序關係；有 fanout／事件數上限與截斷標示 | [測試紀錄](tests.log) |
| 重疊候選可重建 | window 4,400＋temporal 4,400 個子圖全部由 SQLite 重建比對；依賴群組核對來源 manifest | [window](window-final-validation.json)、[temporal](temporal-final-validation.json) |
| 原始來源追溯 | 11 份原始檔重新核對 SHA-256，每份抽查一筆候選錨點，確認原始內容 hash | [raw trace audit](raw-trace-validation.json) |
| 真正使用指定 backbone | 固定上游 commit／models.py hash，執行上游 OrderEmbedder、SkipLastGNN、typed SAGE；四組實際訓練 | [整合說明](../README.md#provg-searcher-整合差異) |
| 表示與快速比較 | 每組 4,400×32 的 embedding；非對稱 order score；shortlist 後精確結構驗證 | [研究結果](research-v1.md) |
| 防止答案作特徵 | label 單獨存表；程序名稱、檔案／錄製名稱、timestamp_raw、row ID 不作 features；train/test 依群組隔離 | [測試](../tests/test_pipeline.py)、[切分](../configs/splits.json) |
| 稀少操作完整擷取 | 掃描全資料的服務設定 RegSetValue；完整取得 383 個符合保守 prefix 條件的錨點 | [targeted manifest](../artifacts/services-write/manifest.json)、[383 圖驗證](../artifacts/services-write/validation.json) |
| 實際調查入口 | 4,400 抽樣候選＋383 目標候選，總共 4,783 圖；查詢服務設定寫入，輸出 10 個核對後片段 | [HTML](../artifacts/analyst-demo-repro/services.html)、[JSON](../artifacts/analyst-demo-repro/services.json) |
| 可重現展示 | 以 run_demo.py 重跑；graphs.jsonl、embeddings.npy、ids.json hash 與第一次執行一致 | [完成稽核](completion-audit.json) |
| 功能測試與既有回歸 | 新增 10 個測試通過；既有 74 個測試執行成功，其中 1 個 skipped | [新測試](tests.log)、[既有測試](repository-tests.log) |

## 初步結果與限制

本次是已完成的研究實作及工程 pilot，不是已完成的投稿實驗。四組都在相同來源與錨點政策下執行，依已知來源依賴切分。每種擷取器的測試包含 300 個保留候選、30 個合成包含查詢。來源候選仍在 gallery，答案是精確結構匹配，**沒有人工相關性或必要上下文標註**。

窗口模型的 Recall@10：無 KG 0.1389、有 KG 0.3542；feature-count baseline 0.7111。

時序模型的 Recall@10：無 KG 0.0537、有 KG 0.1274；feature-count baseline 0.4798。

這支持流程可執行，且 KG 在這輪改善部分檢索指標，但 GNN 尚未優於簡單 baseline。時序模型的 MRR 甚至沒有隨 KG 改善，不能只挑有利數字。

兩個擷取器的 query 內容與圖大小不同，不能直接以兩者 Recall 差異論證切圖優劣。window 平均 16.24 事件、temporal 平均 32.83 事件；多數圖達 fanout 或大小限制。這揭露下一階段需要固定大小、獨立查詢、必要上下文標註，以及避免高連接 Registry 拉入太多背景的研究問題。

均勻抽樣的 4,400 錨點沒有服務設定寫入樣本；全資料 query-conditioned 擷取找到 383 個。這兩種資料不可混成同一份無偏評分資料，展示的額外候選也不反過來調整原測試成績。

模型輸出的 order violation 不是機率或風險分數。向量索引目前是 O(Nd) 矩陣掃描，不宣稱 ANN。精確核對只針對 shortlist，仍可能漏掉相關圖；[展示的完整匹配稽核](demo-retrieval-audit.json)會揭露這個差距。簡單功能條件應保留直接路徑／操作查詢作對照，不能因為用了 GNN 就假設更快。

## 下一個研究 gate

1. 固定新的開發／保留查詢，標註少量必要上下文及相關性；目前已檢視的 pilot 不再當最終盲測。
2. 比較相同事件預算的切圖方法，加入高連接節點控制、重疊去重及覆蓋／冗餘分析。
3. 從訓練群組改善包含關係配對與難負例，重跑多 seed；先確認優於 feature-count，再擴充深度或模型。
4. 對複合行為查詢量測檢索速度與分析工作量，避免只用單一 key 查詢展示 graph embedding 價值。

程式與設定 hash：[source manifest](source-manifest.json)。已驗證環境：[environment.lock.txt](environment.lock.txt)。原始資料、既有 KG、AGENTS.md、ANTS_KGmaer 和既有未提交修改均未改寫。
