# SAGA v2 實作與驗證紀錄

已完成 SAGA archive 驗證、全量格式／標籤稽核，以及三份錄製的端到端機制試跑。**完整 v2 正式比較未完成**：archive 的 metadata 缺少混合 campaign 組成來源，依計畫停止正式分割與比較，不改用隨機子圖分割。

## 來源與實際資料

2026-11-09 取得官方 archive，707,841,341 bytes；SHA-256 與官方 `c15e8b985b4cab1d1ebf106e01ce5c14d9b730da5af786167b58778c422992b1` 一致。38 份錄製全部掃描：27,805,563 筆事件、27,728,473 benign、77,090 明確 Technique 標註事件、17,055,744 Registry 目的端事件，無未知標籤。

實際事件為 JSONL，欄位是 srcNode/dstNode/relation/timestamp/label；物件以 UUID 識別，Registry 加入 Key 區別；缺失端點保留獨立身份。label 為 benign 或 Technique/sub-technique 加實例後綴，解析父類但保留原始 label。原始檔不改寫，SQLite 保存來源 hash、事件位置與原始事件 hash。

metadata.json 只有 C1–C8、G1–G20，沒有 M1–M10 的記錄或組成對照；也沒有模板、背景及原始片段映射。20 份 G 系列的實際事件筆數小於 metadata 記載；manifest 以實際檔案為準，差異保留，未補造事件。

[來源 manifest](saga-source-manifest.json)、[完整格式與標籤稽核](saga-release-audit.json)、[機器可讀狀態與待辦](saga-status.json)。來源規格見 [官方頁面](https://www.saga-cyber.net/dataset)。

## 獨立機制試跑

依 archive byte size 選 metadata 有列出的最小三份錄製，不看標籤：G16、G6、C7。seed=17 分組後，分別為 train/validation/test。只允許錄製層級可行性解讀，不能排除模板重用。跨 split 完全重複原始事件為 0；未完成全 v2 重複片段稽核，因為全 v2 正式來源分割仍受阻。

初始每份 30 個均勻 Registry 錨點。validation 依預先固定順序擴至 8,000；train/test 各維持 30。三擷取器共用清單，hops=2、fanout=8、offline、budget=33。執行 prior、anchor、counts、pool、R-GCN KG/no-KG × seeds 7/17/27 × 三擷取器，共 54 runs，各學習模型 2 epochs。checkpoint、逐圖機率、錯誤案例、分層及事件集合去重指標都保存在 `artifacts/saga-v2/pilot-runs/`。

[試跑比較](saga-pilot-summary.md)列出全部成績。只有 30 張 test 圖，其中 2 張惡意；test Technique T1005/T1059 未出現在 train 字典，因此 Technique 效果不可評估，不能把未覆蓋類別當成已知類分類錯誤。只有一個 test 來源群組，來源群組信賴區間不可估計。模型成績未呈現一致優勢，不能以此聲稱 R-GCN、KG 或任一擷取法更有效。所有試跑 test 已視為開發資料。

## 驗證與尚未完成工作

34 項 unittest 通過，compileall 通過。涵蓋 multi-label、unknown mask、未見類別、全陰性 validation、混合／共享背景依賴、群組不足、checksum 失敗、跨分割重複、特徵隔離、手算指標、來源群組 bootstrap、共同錨點、整個 validation split 支持數與精確續訓一致性。三種條件每 split 抽五圖，45 張重新擷取、標籤比對及整份資料 hash 全部通過：[驗證產物](saga-pilot-verification.json)。

仍需補足 M1–M10 的組成來源證據，建立完整 v2 依賴分割與跨分割重複片段稽核，才可執行正式 2,000 錨點、budget 33/128、最多 50 epochs、三 seeds 比較。缺少模板／背景映射時，結論仍只限錄製層級可行性。不得混入 CHT/APT 或把本次試跑充作完整研究完成。

模型設計、下載、格式轉換、訓練與續訓、試跑重現命令見 [SAGA README](../docs/SAGA.md)。
