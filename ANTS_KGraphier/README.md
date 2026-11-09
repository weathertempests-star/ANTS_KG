# ANTS_KGraphier

SAGA v2 分類的新流程、下載與來源限制見 [SAGA 實驗文件](docs/SAGA.md)，實際資料稽核與 54 runs 試跑見 [驗證報告](reports/saga-validation.md)。下列舊 CHT/APT 結果不屬於 SAGA 實驗。

Registry 事件中心的可追溯子圖擷取與分析檢索研究。輸出是供分析人員檢查的活動片段，**不是惡意判決**。此目錄獨立於既有 ANTS_KGmaer，不改寫 data、知識 catalog 或 vault。

已執行結果：[研究報告](reports/research-v1.md)、[逐項驗收](reports/IMPLEMENTATION_VALIDATION.md)、[離線調查入口展示](artifacts/analyst-demo-repro/services.html)。大型索引及模型保存在本地 artifacts，不進版控。

## 實作

- `ingest`：串流讀取六份 CHT array 與五份 APT JSONL，驗證檔案 SHA-256／筆數，建立 SQLite 端點與順序索引。來源清單位於 `configs/sources.json`。
- `extract`：Registry 操作事件為錨點；提供 process window 與 bounded temporal ego graph，支援離線前後文或僅歷史模式。保存每一步擴展的 parent event、shared endpoint、方向、跳數與截斷狀態。
- `validate`／`trace`：從事件索引重新擷取比對完整子圖；trace 另重新雜湊原始檔並查回原始事件。
- `train`：執行 **ProvG-Searcher 上游 OrderEmbedder、SkipLastGNN、typed SAGE**，使用真實候選圖生成包含關係訓練對，負例經精確圖匹配核對。
- `index`／`search`：預計算圖 embedding，利用非對稱 order violation 做向量掃描，候選再經 typed directed subgraph monomorphism 核對。提供高重疊片段合併及來源證據。
- `evaluate`：依錄製依賴群組保留測試，評估合成 containment query 的 Recall@K／Precision@K／MRR，對照非學習 feature-count baseline。
- `render`：輸出可離線閱讀的 HTML 證據頁。

## 安裝

從 repository root 執行，使用 Python 3.10 以上（本次環境 Python 3.12）。

```bash
python -m venv ANTS_KGraphier/.venv
ANTS_KGraphier/.venv/bin/python -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
ANTS_KGraphier/.venv/bin/python -m pip install -e ANTS_KGraphier
ANTS_KGraphier/.venv/bin/python ANTS_KGraphier/scripts/fetch_backbone.py
ANTS_KGraphier/.venv/bin/python -m unittest discover -s ANTS_KGraphier/tests -v
```

上游依賴不隨此專案重新散布；fetch 腳本下載指定 commit，既有不同 checkout 不會被覆寫。

## 完整研究流程

```bash
ANTS_KGraphier/.venv/bin/python ANTS_KGraphier/scripts/run_research.py --output ANTS_KGraphier/artifacts/research-v1
```

產生報告及調查展示（每次選新的 output）：

```bash
ANTS_KGraphier/.venv/bin/python ANTS_KGraphier/scripts/summarize.py --research ANTS_KGraphier/artifacts/research-v1 --output ANTS_KGraphier/reports/research-v1.json
ANTS_KGraphier/.venv/bin/python ANTS_KGraphier/scripts/run_demo.py --research ANTS_KGraphier/artifacts/research-v1 --output ANTS_KGraphier/artifacts/analyst-demo-repro
```

預設完整索引 11 份原始錄製，每份均勻抽樣 400 個 Registry 錨點，不看 label。比較 window／temporal × KG／no-KG 四組，**候選抽樣不等於完整日誌所有錨點的檢索測試**。相同抽樣 seed 使切圖條件使用相同錨點。設定全部記錄於 commands、manifest 與 model.json。

個別階段：

```bash
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier ingest --output ANTS_KGraphier/artifacts/events.sqlite
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier extract --store ANTS_KGraphier/artifacts/events.sqlite --output ANTS_KGraphier/artifacts/candidates --per-recording 400
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier train --graphs ANTS_KGraphier/artifacts/candidates/graphs.jsonl --output ANTS_KGraphier/artifacts/model
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier index --graphs ANTS_KGraphier/artifacts/candidates/graphs.jsonl --model ANTS_KGraphier/artifacts/model --output ANTS_KGraphier/artifacts/index
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier search --graphs ANTS_KGraphier/artifacts/candidates/graphs.jsonl --model ANTS_KGraphier/artifacts/model --index ANTS_KGraphier/artifacts/index --prefix 'HKLM\SYSTEM\CurrentControlSet\Services' --operation RegSetValue --output ANTS_KGraphier/artifacts/services.json
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier render --result ANTS_KGraphier/artifacts/services.json --output ANTS_KGraphier/artifacts/services.html
```

`search --query query.json` 支援自訂 symbolic 行為圖，schema 可由 search 結果中的 `query` 取得。`--prefix` 必須對應具體 KG 節點；不默默把未知 prefix 降成 hive。Query graph 的操作種類及 KG 功能條件是分析需求，沒有預設的「攻擊標籤」。

稀少敏感操作可能被均勻抽樣漏掉。實際調查可完整擷取符合條件的錨點：

```bash
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier extract --store ANTS_KGraphier/artifacts/events.sqlite --output ANTS_KGraphier/artifacts/services-write --prefix 'HKLM\SYSTEM\CurrentControlSet\Services' --operation RegSetValue
```

此模式掃描所有來源的指定操作，對 KG prefix 條件完整擷取，忽略 `--per-recording`。它是 query-conditioned corpus，不能拿來冒充無偏測試。無條件 `extract --per-recording 0` 則擷取所有 Registry 錨點，輸出量可能非常大。

查回單筆原始事件：

```bash
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier trace --store ANTS_KGraphier/artifacts/events.sqlite --recording SOURCE_SHA256 --row ZERO_BASED_ROW --output ANTS_KGraphier/artifacts/raw-event.json
```

輸出包含原始人工 label，僅供授權的資料追溯；不將此輸出交給 encoder。

## 時序與身份

timestamp 只作順序參考，不當秒數。相同值的事件不會建立 PRECEDES 關係；列號只作可重現識別與同值候選的預算選擇。Offline 模式允許錨點前後文；past 模式只沿嚴格較早事件擴展。共享端點表示觀察到的關聯，**不證明因果**。

模型使用 event-incidence graph：實體 → 操作節點 → 實體，以及同 actor 的嚴格順序邊。每筆事件獨立，保留平行讀寫；不是把所有事件壓成單一 src–dst edge。具體端點 ID、原始路徑、timestamp、來源名稱、label、timestamp_raw、程序名稱、命令列不進模型特徵。節點特徵只有類型、操作、錨點旗標及 KG prefix IDs。

KG 不變；其階層透過 ancestor-prefix multihot 特徵注入，**沒有另行訓練 KG GNN，也沒有將 HAS_CHILD 當作事件因果邊**。本版不實作模板、value data 判讀或推測成功與否。未確認的 value operation 只保存 prefix context，最後一段匹配不當成確認的 key。這種保守詞法上下文仍不等同已驗證的完整 key/value 邊界。

## ProvG-Searcher 整合差異

來源：https://github.com/EnesAltinisik/ProvG-Searcher

固定 commit：`ac85b4e4e6f387cbf3bd8b94c87c62015f7440bb`。

`common/models.py` SHA-256：`163be3867a12135afbefe18c981a4323b9cde326fc9b07c70253d48a225d6988`。

`backbone.py` 驗證 hash 後以 AST 載入五個模型 class，class body 保持原樣。僅提供 CPU device 與停用 feature augmentation 的 namespace，避免執行上游 DARPA dataset／DeepSNAP 載入鏈。使用上游 mean pooling、learnable skip、雙方向 typed SAGE、order loss；參數採 2 層／32 維，沒有宣稱重現原論文成績。

本研究的差異包括 Registry 事件錨點、incidence graph、三種邊類型、KG prefix 特徵、可稽核 containment 訓練對、現代 PyG 2.6.1 適配。沒有以隨機權重或 hash vector 冒充訓練後 backbone。

## 評估邊界

`configs/splits.json` 固定錄製群組；已知 CobaltGroup／Higaisa／Gamaredon 重用背景合併為同一訓練群組。CHT 與 APT 都有保留錄製，不宣稱是未見組織或完整 APT 家族泛化。正式人工相關性 benchmark 仍需獨立標註；目前既有 malicious labels 不足以衡量分析相關性。

測試 query 從保留錄製的候選圖擷取，精確 containment 作答案，來源候選留在 gallery。這是結構檢索工程驗證，不是人工查詢品質。重複行為可能在不同錄製出現，不能將事件數當成獨立樣本數。Feature-count baseline 必須保留；如果它勝出，報告會呈現結果。

向量搜尋目前為完整矩陣掃描，成本 O(Nd)，不是 ANN 或次線性索引。精確驗證只核對 shortlist，因此不保證找到全部匹配。離線編碼、查詢編碼、向量掃描和精確驗證的成本應分開報告。

研究產物在 `artifacts/`，被 git 忽略；來源和 KG hash 保存在 manifest。不得把未完成 stage 當成有效快取，所有主要產物拒絕覆寫。環境與 vendor 也不進版控。

## 學習式切圖：遠端完整訓練逐步指引

以下命令皆從 repository root 執行。這個流程訓練 anchor-conditioned event selector，再將實際選出的事件交給 ProvG-Searcher。selector 的監督、特徵與 checkpoint 和檢索模型分開保存。Bernoulli KL 正則化已接上訓練；--stochastic 以 Concrete 隨機遮罩計算 membership loss。這是受 GSAT 啟發的監督式事件選擇器，沒有重現原論文的 graph classification objective，不得稱為完整 GSAT 重現。

### 1. 搬移程式與本地資料

把整個專案 checkout 搬到研究伺服器，保留 `ANTS_KGraphier/`、`standardizer_pkg/`（若既有工具需要）、`artifacts/knowledge-vault/kg.json`。不要僅搬模型檔。原始 CHT/APT 是本研究本地資料，沒有可假設的公開下載網址，需自行從持有的副本傳入伺服器；保留 `data/CHT_selected/*.json`、`data/Apt/*/events.json` 相對路徑。使用 `configs/sources.json` 的 SHA-256 驗證來源，勿修改 hash 來掩蓋不同版本。

```bash
python3 -m venv ANTS_KGraphier/.venv
source ANTS_KGraphier/.venv/bin/activate
python -m pip install --upgrade pip
python -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -e ANTS_KGraphier
python ANTS_KGraphier/scripts/fetch_backbone.py
python -m unittest discover -s ANTS_KGraphier/tests -v
python -m pip freeze > ANTS_KGraphier/environment.remote.txt
```

上述 CPU 環境可執行完整流程；GPU 主機可依其 CUDA/driver 安裝相容的 PyTorch wheel，安裝後用 `python -c 'import torch; print(torch.__version__, torch.cuda.is_available())'` 檢查，再對 selector 命令傳 `--device cuda`。目前逐圖訓練，不承諾 GPU 一定較快，也尚未驗證分散式訓練。

### 2. 取得公開資料與固定版本

官方來源於 2026-11-04 查核：

- [SAGA 官方下載頁](https://www.saga-cyber.net/dataset)：先取 v2 evaluation 的有限切片做 schema audit；正式 training corpus 應選定需要的 campaigns，官方列出的完整訓練下載規模為 5.1 TB。頁面 Download 連到 Google Drive，下載後以官方 checksum／Checksums.ini 驗證，再保存自己的檔案 SHA-256 清單。不要以檔名推測版本一致。
- [DARPA OpTC 官方資料庫](https://github.com/FiveDirections/OpTC-data)：依 README 的 Google Drive 連結選取 `ecar` 端點資料，並一併保存 `ecar.md`、`errata.md`、`OpTCRedTeamGroundTruth.pdf`。`ecar-bro` 是 FLOW-START 對照資料，不能替代完整端點日誌。

建議建立 `data_external/{saga,optc}/raw/` 與獨立的轉換輸出目錄。紀錄下載 URL、取得日期、archive hash、解壓後檔案 hash、授權及來源版本。大型下載可用瀏覽器／官方 Drive 介面選取檔案，再用可續傳工具轉入訓練主機；不要在未確認容量前下載全部 corpus。

本版原生 ingest 支援本地 `srcNode`、`dstNode`、`relation`、`timestamp` 格式；**尚未驗證外部 SAGA 版本及 OpTC eCAR 的自動轉換**。外部資料接入前必須完成下列對照，不能直接改副檔名送入：

| 內部欄位 | 外部轉換要求 |
|---|---|
| srcNode/dstNode | Type、穩定物件 UUID；身份需包含 host/recording 範圍，未知端點不可共用一個假 ID |
| Registry Key | 保留完整原始 key；value name/data 分開保存，不猜測不存在欄位 |
| relation | 保存原操作及顯式映射表，未知類型保留 Unknown 並統計 |
| timestamp | 可排序的順序值；本地實驗不使用秒數特徵，不能把跨主機未同步時間宣稱為因果 |
| label | 獨立監督欄位，不進模型；未標註不是 benign |
| provenance | 每個轉換事件保留原始檔、原始行號與 hash 的 sidecar |

SAGA 若有 generator occurrence-to-event mapping，可以轉為 `generator_instance` 監督；只有 technique/phase 不足以宣稱完整活動實例。OpTC 的紅隊文件需要先對齊事件，無法對齊者保持 unknown。外部適配完成前，可先用本地完整資料執行以下訓練，不能把外部資料的結果列入已完成驗證。

### 3. 建立資料索引與分割

```bash
python -m ants_kgraphier ingest --data data --sources ANTS_KGraphier/configs/sources.json --output ANTS_KGraphier/artifacts/remote-events.sqlite
```

輸出已存在會拒絕覆寫。索引使用來源 SHA-256 與零起算事件 ordinal 追溯。可直接搬移已完整完成的 SQLite 與 manifest，但不要複製正在寫入的 SQLite。

`configs/segmentation-splits.json` 在原分割上保留一個完整 CHT 錄製作 validation，共享背景的 APT 仍在同組。這是本地開發分割；舊 pilot 的 test 已經被檢視，不能宣稱全新 blind test。正式實驗需在補上腳本／模板重用稽核後，固定新分割；相同腳本的不同錄製與未見腳本泛化分開報告。SAGA mixed campaign 需要依其組成模板分組。

```bash
python ANTS_KGraphier/scripts/prepare_segmentation.py --store ANTS_KGraphier/artifacts/remote-events.sqlite --splits ANTS_KGraphier/configs/segmentation-splits.json --output ANTS_KGraphier/artifacts/remote-candidates --per-recording 400 --train-labeled 80 --budget 128
```

等待命令成功結束且 `.building` 消失才開始訓練。中斷時不要刪除該標記後假裝完整，請使用新 output 重建。產物：`graphs.jsonl`、空白人工表單 `review.jsonl`、明示弱規則的 `weak.jsonl`、來源與分割 `manifest.json`。訓練集額外抽取有標籤錨點，validation/test 僅均勻抽樣；抽樣策略記錄於每圖，不能把訓練增補樣本當無偏資料。

### 4. 建立真正的切圖標註

複製 `review.jsonl` 為另一個工作檔，逐錨點填寫 `episode_id`、`reviewer`，並在 `memberships` 列出 `event_id`、`role`、`confidence`。role 有 core、context、unrelated、unknown；未列出事件自動視為 unknown。只在候選每一筆都已明確分類時設 `complete=true`。必要事件若不在候選內，填入 `required_outside_candidate`，使評估能揭露候選召回上限。

同一實際活動的多個錨點使用同一 episode_id；不同錄製不要重用簡短 ID。建議先標註 150–300 個活動，涵蓋正常操作、攻擊相關操作、相同 key 的不同用途與交錯活動，再讓第二位標註者複核部分樣本。標註不應只看目前候選，需回查原日誌，否則無法發現漏掉的必要事件。

`weak.jsonl` 只提供可執行的開發實驗：同來源程序且同人工事件標籤作弱相關假設，不同程序作弱無關假設；跨程序活動因此可能被錯誤處理。benign 不直接等於負例，episode_id 此時僅是錨點代理。它不是論文的人工切圖 ground truth。

### 5. 訓練與選模

```bash
python -m ants_kgraphier.segmentation train --graphs ANTS_KGraphier/artifacts/remote-candidates/graphs.jsonl --annotations ANTS_KGraphier/artifacts/remote-candidates/weak.jsonl --output ANTS_KGraphier/artifacts/selector-weak-seed7 --epochs 30 --seed 7 --budget 32 --selection-metric macro_f1
```

正式訓練把 `--annotations` 換成完成的人工／可追溯實例標註檔。模型用 train 計算梯度，只使用 validation 在各 epoch 與門檻 0.3/0.5/0.7 中選擇 checkpoint。正式預設 selection-metric 是 macro_context_f1，若 validation 沒有上下文正例會拒絕選模；上述 weak smoke 顯式改用 macro_f1。測試集不參與選模。輸出包含 weights、hash、超參數、歷史及監督來源。unknown 的 loss 權重為零；目前 class balancing 為每圖平衡，尚未按實際 episode 做訓練抽樣平衡。

完整實驗至少比較 seed 7/17/27、budget 16/32/64、KG/`--no-kg`。每次使用不同 output。CPU 本地 smoke 的 epoch 數只驗證執行，不是推薦的最終訓練長度。先以 validation 學習曲線決定長度，再凍結設定測試。

訓練 loader 使用暫存 SQLite 索引 JSONL 的 byte offset，每次只編碼一張候選圖；RAM 仍保存 shuffle 所需的整數索引和 validation 評估摘要。設定 TMPDIR 可選擇索引磁碟位置。正式主機仍應以有限 shard 測量 RSS、暫存空間與吞吐量；TB 級吞吐與分散式訓練尚未驗證。每個 epoch 原子保存 last.pt 與 hash sidecar；可用 --resume OLD_RUN/last.pt --output NEW_RUN --epochs TOTAL_EPOCHS 續訓，必須維持相同資料 hash、超參數與 device。CPU 續訓與不中斷訓練的一致性已有回歸測試。

### 6. 輸出與評估

```bash
python -m ants_kgraphier.segmentation select --graphs ANTS_KGraphier/artifacts/remote-candidates/graphs.jsonl --model ANTS_KGraphier/artifacts/selector-weak-seed7 --output ANTS_KGraphier/artifacts/selected-weak-seed7.jsonl
python -m ants_kgraphier.segmentation evaluate --graphs ANTS_KGraphier/artifacts/remote-candidates/graphs.jsonl --annotations ANTS_KGraphier/artifacts/remote-candidates/weak.jsonl --model ANTS_KGraphier/artifacts/selector-weak-seed7 --split test --output ANTS_KGraphier/artifacts/eval-weak-seed7.json
```

分數先在 episode 內平均錨點，再對 episode macro average；unknown 不當負例，precision 是已審核部分的 precision，需連同 reviewed_selected 與總 selected 數量解讀。必要候選外事件會降低 recall。弱監督報告只能衡量規則一致性。另報 macro_context_f1 與 context_supported_graphs：排除強制保留的錨點，只在存在已標註上下文正例的圖上衡量上下文 F1；沒有上下文標註時此值為 null，不能用高整體 F1 代替。

選出圖仍保留完整事件來源資訊；`learned_selection` 記錄 probability、anchor/selected/connector。connector 是為連通性補入，不應誤稱模型直接認定其相關。模型 hash 寫在每張輸出圖。選出圖可送既有 `train/index` 重新編碼，不可直接沿用完整候選的 embedding 冒充切圖後表示。

固定人工 query 與 gallery 比較不同切圖器，另外保留 feature-count baseline。現有檢索 evaluate 使用由候選產生的合成 query，不能作為跨切圖器的公平品質比較。正式比較需要共同人工 query/相關性判定、跨活動誤合併、碎裂、重疊膨脹及全流程成本。


### 表示預訓練與隨機選擇消融

`segmentation train` 可加 `--pretrain-epochs 3 --stochastic`。預訓練逐圖讀取 train 分割，對候選內所有事件類型做 masked operation reconstruction；validation/test 不做梯度更新，事件 label 不被讀取。操作目標為固定 hash 的 64 buckets，因此可能碰撞；這是輔助表示學習任務，不是 technique classification。它覆蓋候選中的事件，不代表已使用完整日誌的每筆背景事件。

`--stochastic` 將 Concrete 隨機遮罩接入事件歸屬 loss；推論仍使用確定的 sigmoid 分數與連通解碼。請分別執行有／無預訓練、有／無隨機遮罩的消融，再決定完整訓練設定。續訓時必須保留相同選項；checkpoint 保存監督訓練的 optimizer、RNG 與預訓練歷史。預訓練尚未完成便中斷時需重新開始該階段。

### 7. 將選出子圖交給 ProvG-Searcher

```bash
python -m ants_kgraphier train --graphs ANTS_KGraphier/artifacts/selected-weak-seed7.jsonl --output ANTS_KGraphier/artifacts/selected-retriever --epochs 10 --pairs 600
python -m ants_kgraphier index --graphs ANTS_KGraphier/artifacts/selected-weak-seed7.jsonl --model ANTS_KGraphier/artifacts/selected-retriever --output ANTS_KGraphier/artifacts/selected-index
python -m ants_kgraphier evaluate --graphs ANTS_KGraphier/artifacts/selected-weak-seed7.jsonl --model ANTS_KGraphier/artifacts/selected-retriever --index ANTS_KGraphier/artifacts/selected-index --output ANTS_KGraphier/artifacts/selected-retrieval-smoke.json --queries 30 --gallery-size 300
```

這是重編碼後的結構檢索 smoke，並非跨切圖方法的公平效果比較。查詢可改用既有 `search --query` 送入固定的人工 symbolic query，搭配同一份相關性判定。

本地已跑通 `artifacts/segmentation-local-v1/`：266 張候選、146 train、20 validation、100 test；輸出 2,237 筆事件逐筆比對 SQLite 通過。KG/no-KG selector 各訓練 8 epochs，另完成預訓練與隨機遮罩試跑；選出圖已經 ProvG-Searcher 重編碼為 266×32 索引。這些 test 資料已被檢視，只能作開發驗證。

弱監督的上下文 F1：KG 0.075、no-KG 0.0506、nearest-budget32 0.5741、anchor-only 0。上下文標註稀少且是規則假設；不能解讀為人工調查效益。下游 10 個合成查詢的 Recall@10 為 ProvG 0.375、feature-count 0.9444；尚未支持 GNN 優於基準。正式研究需要人工活動上下文與固定查詢，再進行多 seed、外部資料及成本實驗。

### 新增錄製與外部資料的來源 manifest

外部檔案先按上面的欄位契約轉換；原始 eCAR 不可直接送入本工具。新增一個 spec，例如：

```json
{"recordings":[{"id":"SAGA-chosen-recording","cohort":"SAGA","path":"chosen/events.jsonl","format":"jsonl","dependency_group":"audited-template-background-group"}]}
```

spec 的 path 相對於 `--root`。不同錄製保留不同 id；共用腳本／背景的錄製共用 dependency_group。工具會逐事件檢查 schema，計算實際筆數與 SHA-256，保留未標註事件，拒絕重複內容及越界路徑。

```bash
python ANTS_KGraphier/scripts/make_sources.py --root data_external/saga/normalized --spec saga-spec.json --output saga-sources.json
python -m ants_kgraphier ingest --data data_external/saga/normalized --sources saga-sources.json --output ANTS_KGraphier/artifacts/saga-events.sqlite
python ANTS_KGraphier/scripts/prepare_segmentation.py --store ANTS_KGraphier/artifacts/saga-events.sqlite --splits saga-splits.json --output ANTS_KGraphier/artifacts/saga-candidates --per-recording 400 --train-labeled 0 --budget 128
```

`saga-splits.json` 必須顯式列出 spec 的所有 dependency_group → train/validation/test。多資料集聯合訓練時，將各資料的 graphs.jsonl 與完成的 annotation JSONL 串接到新的檔案，保留原始 graph/episode ID，不能為了避開重複檢查重新命名。同一來源跨 train/test 會被拒絕。腳本重用仍需人工來源稽核，工具不能僅從 UUID 證明獨立性。

若使用新 KG snapshot，重新產生所有候選與模型；selector 訓練拒絕混合 KG snapshot，新 checkpoint 也會拒絕套用到不同 snapshot。

## TREC 啟發的分支停止擷取

新增 `extract --method trec`，可直接接入既有 selector／ProvG-Searcher 流程。參考 [TREC §3.1.2](https://arxiv.org/html/2402.15147v2)：從關注點搜尋，在 λ 跳內遇到下一個關注點便繼續展開，否則停止分支；保留訪問過的普通上下文。

本版適配：固定 Registry 事件錨點；用 RegSetValue、RegCreateKey、RegDeleteKey、RegDeleteValue、Process Create 作操作關注點，不代表惡意或敏感度判決。沒有重現 TREC 的 GNN/iForest 程序 NOI 偵測或最高度數 seed 選擇。`--hops` 表示連續未遇關注點的事件轉移上限，遇到關注點歸零，總搜尋仍受 fanout 與 budget 限制。事件跳數不等於論文 entity hops。

每個分支維持嚴格順序，offline 在前後方向間交替分配搜尋機會，分支內採 DFS；past 只查更早事件。相同 timestamp 不建立先後關係。每個事件保存 parent、via、方向、累積 hop 及 gap_since_poi；輸出新增 policy_version、poi_hits、branch_stops、fanout_truncations、budget_truncated 等診斷。這是觀察關聯，不宣稱因果或活動真實邊界。

```bash
python -m ants_kgraphier extract --store ANTS_KGraphier/artifacts/events.sqlite --method trec --hops 2 --fanout 8 --budget 33 --per-recording 400 --output ANTS_KGraphier/artifacts/trec-candidates
python -m ants_kgraphier validate --store ANTS_KGraphier/artifacts/events.sqlite --graphs ANTS_KGraphier/artifacts/trec-candidates/graphs.jsonl --output ANTS_KGraphier/artifacts/trec-validation.json
python ANTS_KGraphier/scripts/prepare_segmentation.py --store ANTS_KGraphier/artifacts/events.sqlite --method trec --output ANTS_KGraphier/artifacts/trec-training --budget 128
```

本地成對診斷位於 `reports/trec-extraction.json`，使用相同錨點／預算，比較 temporal 與 trec，逐圖重新擷取驗證。這是擷取機制與成本驗證；缺少人工活動邊界，因此不能從圖較小、較大或關注點較多宣稱切圖準確率提升。較長 POI 鏈與強制預算可能仍截斷上下文；需連同診斷欄位審核。

## 固定子圖惡意判別與 Technique 多標籤分類

獨立模組 `ants_kgraphier.classification` 提供 `prepare、audit、train、predict、evaluate、compare`；原有檢索與 selector 命令不變。設計、標籤遮罩、模型與有效結論範圍見 [分類設計](reports/classification-design.md)，實測見 [本地驗證](reports/classification-validation.md)。使用前述環境與已完成的 SQLite/KG。

本地 smoke（新 output，validation 仍可能擴至 8,000 或全部錨點）：

```bash
python -m ants_kgraphier.classification prepare --store ANTS_KGraphier/artifacts/events.sqlite --per-recording 30 --budgets 33 128 --output ANTS_KGraphier/artifacts/classification-smoke
python -m ants_kgraphier.classification compare --data ANTS_KGraphier/artifacts/classification-smoke --epochs 2 --seeds 7 17 27 --output ANTS_KGraphier/artifacts/classification-smoke-runs
python -m unittest discover -s ANTS_KGraphier/tests -v
```

遠端完整流程（同一 repository root、來源與 KG；CPU 預設，GPU 可加 `--device cuda`）：

```bash
python -m ants_kgraphier.classification audit --store ANTS_KGraphier/artifacts/events.sqlite --output ANTS_KGraphier/artifacts/classification-audit.json
python -m ants_kgraphier.classification prepare --store ANTS_KGraphier/artifacts/events.sqlite --per-recording 2000 --seed 17 --budgets 33 128 --output ANTS_KGraphier/artifacts/classification-full
python -m ants_kgraphier.classification compare --data ANTS_KGraphier/artifacts/classification-full --epochs 50 --seeds 7 17 27 --output ANTS_KGraphier/artifacts/classification-full-runs
```

compare 依序執行三擷取器 × 兩預算 × 六模型/KG 條件 × 三 seeds，共 108 runs。預設單執行緒以避免小圖計算的 thread overhead；可調 `--threads`。prepare 的 validation 不足會讓 train 明確中止；不要換抽樣 seed 直到出現好成績。跨分割重複事件會阻擋準備，先依來源證據修正 dependency groups，再重建。

個別訓練、續訓與推論：

```bash
python -m ants_kgraphier.classification train --data ANTS_KGraphier/artifacts/classification-full/temporal-33 --output ANTS_KGraphier/artifacts/classifier --epochs 10 --seed 17
python -m ants_kgraphier.classification train --data ANTS_KGraphier/artifacts/classification-full/temporal-33 --output ANTS_KGraphier/artifacts/classifier-resumed --epochs 50 --seed 17 --resume ANTS_KGraphier/artifacts/classifier/last.pt
python -m ants_kgraphier.classification predict --data ANTS_KGraphier/artifacts/classification-full/temporal-33 --model ANTS_KGraphier/artifacts/classifier-resumed --split test --output ANTS_KGraphier/artifacts/classification-predictions.jsonl
python -m ants_kgraphier.classification evaluate --data ANTS_KGraphier/artifacts/classification-full/temporal-33 --model ANTS_KGraphier/artifacts/classifier-resumed --split test --output ANTS_KGraphier/artifacts/classification-test.json
```

`--mode prior|anchor|counts|pool|rgcn` 選模型；`--no-kg` 將 KG 區塊歸零，不改變輸入維度。checkpoint 的門檻已由 validation 凍結，predict/evaluate 不重新調整。現階段 predict 接受同格式 graphs/labels dataset（可使用 unknown sidecar），保留新資料的可追溯性。

重新擷取分層抽樣並比對 SQLite 人工標籤，以及產生三 seeds 摘要：

```bash
python ANTS_KGraphier/scripts/verify_classification.py --data ANTS_KGraphier/artifacts/classification-smoke --store ANTS_KGraphier/artifacts/events.sqlite --output ANTS_KGraphier/artifacts/classification-verification.json
python ANTS_KGraphier/scripts/summarize_classification.py --data ANTS_KGraphier/artifacts/classification-smoke --runs ANTS_KGraphier/artifacts/classification-smoke-runs --output ANTS_KGraphier/artifacts/classification-summary
```

驗證腳本檢查六條件完整共同錨點集合及資料 hash，再以 seed=17 每 split 抽五圖重新擷取，核對 sidecar 的人工標籤。摘要會同時產生 JSON 與 Markdown，列出實際圖大小、重複事件集合、各類支持與未覆蓋 Technique。
