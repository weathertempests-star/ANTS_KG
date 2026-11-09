# SAGA v2 子圖分類實驗

本次實際下載、全量資料稽核與機制試跑結果見 [驗證報告](../reports/saga-validation.md)。

本流程只使用 SAGA v2 Complete Evaluation Set，自訂來源群組 train/validation/test 協定，並非官方訓練／測試協定。合成資料結果不代表真實環境成效。原有 CHT/APT 實驗產物不得混入。

## 取得與格式稽核

從 repository root 執行，環境沿用主 README 的安裝指令。

```bash
mkdir -p ANTS_KGraphier/artifacts/saga-v2
curl -fL --retry 3 --output ANTS_KGraphier/artifacts/saga-v2/complete.zip 'https://drive.usercontent.google.com/download?id=1bFmRdn5Kw1FVOS37dRXCobZZ9UBBjrni&export=download&confirm=t'
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier.saga inspect --archive ANTS_KGraphier/artifacts/saga-v2/complete.zip --output ANTS_KGraphier/artifacts/saga-v2/verified
```

來源：[官方資料頁](https://www.saga-cyber.net/dataset)。官方列出 38 campaigns（含 10 mixed）、14.5 GB；下載檔大小與解壓後大小另據實記錄。SHA-256 固定於 adapter；不符即停止，保留 source-manifest.json，不能忽略 checksum 繼續正式實驗。

完整事件／標籤筆數稽核：

```bash
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier.saga audit --raw ANTS_KGraphier/artifacts/saga-v2/verified/raw --output ANTS_KGraphier/artifacts/saga-v2/release-audit.json
```

inspect 產生 archive inventory、來源 manifest、原始檔 SHA-256 與 raw 目錄。必須先查閱實際 metadata 和事件，再寫 reviewed-specification.json，例如：

```json
{
  "metadata_files": ["metadata.json"],
  "recordings": [
    {"id": "base-a", "path": "base-a/events.json", "format": "jsonl"}
  ],
  "dependencies": {
    "base-a": {"templates": ["template-id"], "backgrounds": ["background-id"], "fragments": ["fragment-id"]},
    "mixed-a": {"mixed": true, "components": ["base-a", "base-b", "base-c"]}
  },
  "confirmed_duplicate_pairs": []
}
```

此為介面示例，不是實際 metadata 宣稱。IDs 與路徑必須依 archive 填入；不可依相似 campaign 名稱猜來源。不明模板／背景映射留空，只允許錄製層級可行性結論。混合 campaign 必須提供來源。共享模板、背景、片段及混合組成透過連通分量合併。群組排序後 seed=17 洗牌，約 70/15/15，各至少一組；不足三組留下停止原因。confirmed_duplicate_pairs 是稽核確認後的錄製 ID 對，加入後必須重建 store、候選及模型。

```bash
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier.saga ingest --raw ANTS_KGraphier/artifacts/saga-v2/verified/raw --source-manifest ANTS_KGraphier/artifacts/saga-v2/verified/source-manifest.json --specification reviewed-specification.json --output ANTS_KGraphier/artifacts/saga-v2/index
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier.classification audit --store ANTS_KGraphier/artifacts/saga-v2/index/events.sqlite --splits ANTS_KGraphier/artifacts/saga-v2/index/splits.json --output ANTS_KGraphier/artifacts/saga-v2/audit.json
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier.classification prepare --store ANTS_KGraphier/artifacts/saga-v2/index/events.sqlite --splits ANTS_KGraphier/artifacts/saga-v2/index/splits.json --output ANTS_KGraphier/artifacts/saga-v2/prepared
```

adapter 支援經稽核的 srcNode/dstNode/relation/timestamp 事件，未知 schema 中止。SQLite 保留原始檔 hash、零起算事件位置及整筆原始事件 hash；label 僅進 sidecar。缺標籤為 unknown；至少一筆已標 Technique 為惡意，全 benign 才為陰性。父 Technique 聯集保留 sub-technique 解析與原始 label map。不由檔名或 campaign 推測事件惡意性。

## 抽樣與模型

三方法共用每份錄製最多 2,000 個均勻 Registry 錨點；不補入已知惡意訓練錨點。validation 整組缺任一 binary 類別時，依原抽樣順序擴至每份 8,000，再全部；test 不調整。hops=2、fanout=8、offline，budgets=33/128。跨 split 完全重複事件會阻擋 prepare。technique-coverage.json 報原始事件到已擷取事件的去重覆蓋率。

allowlist 特徵為節點類型、train 操作詞彙、錨點及可選 KG ancestor-prefix；實體 ID、原始字串、來源、標籤不輸入模型。entity–event–entity、PRECEDES 及反向邊建立 incidence graph。兩層關係 mean R-GCN：hidden 64、ReLU、dropout .2；事件 mean/max 加錨點，192 維表示；binary 與 Technique 各為 192→64→輸出，sigmoid。masked binary BCE 加 Technique BCE；train 正類權重上限 20。未知標註不作負類，Technique 字典只取 train。

AdamW lr=.001、weight decay=.0001、batch=32、最多 50 epochs、patience=8。checkpoint 依 validation balanced accuracy 與已支持 Technique macro-F1 平均選擇；無支持 Technique 則只用 binary。0.05–0.95 門檻網格只看 validation，test 前凍結。

```bash
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier.classification compare --data ANTS_KGraphier/artifacts/saga-v2/prepared --output ANTS_KGraphier/artifacts/saga-v2/runs --seeds 7 17 27 --epochs 50
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier.classification train --data ANTS_KGraphier/artifacts/saga-v2/prepared/trec-33 --output ANTS_KGraphier/artifacts/saga-v2/first --epochs 10 --seed 17
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier.classification train --data ANTS_KGraphier/artifacts/saga-v2/prepared/trec-33 --output ANTS_KGraphier/artifacts/saga-v2/resumed --epochs 50 --seed 17 --resume ANTS_KGraphier/artifacts/saga-v2/first/last.pt
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier.classification predict --data ANTS_KGraphier/artifacts/saga-v2/prepared/trec-33 --model ANTS_KGraphier/artifacts/saga-v2/resumed --output ANTS_KGraphier/artifacts/saga-v2/predictions.jsonl
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier.classification evaluate --data ANTS_KGraphier/artifacts/saga-v2/prepared/trec-33 --model ANTS_KGraphier/artifacts/saga-v2/resumed --output ANTS_KGraphier/artifacts/saga-v2/test.json
```

compare 包含 prior、anchor、counts logistic regression、pool、R-GCN KG/no-KG，共 108 runs。小型端到端機制測試可用獨立 output、少量錨點／epochs；必須標為試跑，不用其 test 調參。正式 compare 僅於來源、重複稽核及 validation 支持數通過後執行。

報告含 binary balanced accuracy、precision/recall/F1、macro-F1、average precision、混淆矩陣與陽性率；Technique oracle 與 end-to-end macro/micro-F1、類支持、train 未見類別與事件量。按錨點、截斷、大小分層，另報完全相同事件集合去重結果；95% percentile CI 以來源依賴群組 bootstrap 1,000 次（seed 17），不足兩組則不提供 CI。未確認依賴會限制 CI 解讀。模型若未超過 counts 基準也保留結果。

## 驗證

```bash
ANTS_KGraphier/.venv/bin/python -m unittest discover -s ANTS_KGraphier/tests -v
ANTS_KGraphier/.venv/bin/python -m compileall -q ANTS_KGraphier/ants_kgraphier
```

測試涵蓋多 Technique 聯集、未知標籤與未見類別、全陰性 validation 中止、混合 campaign 與共享背景分組、不足三組、checksum 失敗、共同錨點、跨分割重複、特徵隔離、手算指標及續訓一致性。

重現三份最小錄製的獨立機制試跑（從已驗證 archive 選擇，未用標籤選檔）：

```bash
ANTS_KGraphier/.venv/bin/python ANTS_KGraphier/scripts/prepare_saga_pilot.py --verified ANTS_KGraphier/artifacts/saga-v2/verified --output ANTS_KGraphier/artifacts/saga-v2/pilot-index-repro
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier.classification prepare --store ANTS_KGraphier/artifacts/saga-v2/pilot-index-repro/events.sqlite --splits ANTS_KGraphier/artifacts/saga-v2/pilot-index-repro/splits.json --per-recording 30 --budgets 33 --output ANTS_KGraphier/artifacts/saga-v2/pilot-prepared-repro
ANTS_KGraphier/.venv/bin/python -m ants_kgraphier.classification compare --data ANTS_KGraphier/artifacts/saga-v2/pilot-prepared-repro --output ANTS_KGraphier/artifacts/saga-v2/pilot-runs-repro --epochs 2 --seeds 7 17 27
ANTS_KGraphier/.venv/bin/python ANTS_KGraphier/scripts/verify_classification.py --data ANTS_KGraphier/artifacts/saga-v2/pilot-prepared-repro --store ANTS_KGraphier/artifacts/saga-v2/pilot-index-repro/events.sqlite --output ANTS_KGraphier/artifacts/saga-v2/pilot-verification-repro.json
ANTS_KGraphier/.venv/bin/python ANTS_KGraphier/scripts/summarize_classification.py --data ANTS_KGraphier/artifacts/saga-v2/pilot-prepared-repro --runs ANTS_KGraphier/artifacts/saga-v2/pilot-runs-repro --output ANTS_KGraphier/artifacts/saga-v2/pilot-summary-repro
```

此試跑只有 budget=33，不能替代正式 budget=33/128 敏感度分析。每個 split 僅一份錄製；test CI 無法估計。所有試跑 test 都視為已檢視的開發資料，不再作獨立正式驗收。
