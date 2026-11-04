# Registry KG 支援 SLM 判別：CHT／Caldera 實驗實作計畫

規劃日期：2026-10-26。本文件是實作規格，模型推論、微調與實驗成效尚未執行。資料清點程式與實際統計另存於 `scripts/profile_experiment_data.py` 和 `artifacts/experiment-planning/data_profile.json`。

使用者已確認兩類資料皆為**逐事件人工標註**；`timestamp` **只代表先後參考，不代表可計算的實際時間**。實驗不計算秒數視窗、每分鐘告警或時間到偵測指標。Caldera operation／ability 原始紀錄尚未確認可取得，不把它設為第一輪必要輸入。

進一步的 [SLM Agent 框架規劃](SLM_AGENT_FRAMEWORK_PLAN.md) 延伸 P3–P5，定義工具、狀態機、預算、輸出驗證與 agent 對照。固定流程先建立基準，再評估自主檢索；標籤、資料切分及可見欄位仍遵守本計畫。

## 1. 研究問題與範圍

主要問題：在固定 SLM、事件上下文與輸入預算下，Registry 功能 KG 是否改善「目前目標 Registry 事件」的人工惡意標籤辨識？特別檢查正常操作的誤報與稀少攻擊的漏報。

次要問題：收益來自路徑標準化、功能文字，還是階層／語意關聯？從 Caldera 再現錄製開發出的系統，能否遷移到 CHT 錄製？收益是否只出現在 KG 完整命中的事件？

初版使用凍結的現有功能 KG。ATT&CK technique 僅作答案與分析分組，不能送進模型提示；不新增測試案例專屬攻擊知識。現有 394 筆知識問答適合後續功能教學微調，並非真實事件的惡意判別測試集。

CHT 依使用者描述為真實錄製，APT 為 Caldera 重現；兩者都不能僅憑名稱推論為獨立企業環境、大規模自然部署或全部惡意事件。

## 2. 實際資料清點

| 類型／錄製 | 全部事件 | Registry 事件 | Registry 人工攻擊 | Registry benign |
|---|---:|---:|---:|---:|
| CHT / 0431311b | 37,489 | 27,479 | 546 | 26,933 |
| CHT / 2b294b34 | 34,797 | 24,198 | 17 | 24,181 |
| CHT / 42c704e4 | 2,378 | 1,699 | 97 | 1,602 |
| CHT / 51fe1c84 | 188,549 | 129,611 | 2 | 129,609 |
| CHT / 5dda2d7d | 26,717 | 21,075 | 0 | 21,075 |
| CHT / 8a07ed19 | 25,050 | 14,471 | 28 | 14,443 |
| APT / APT28 | 1,209,895 | 771,817 | 0 | 771,817 |
| APT / CobaltGroup | 969,542 | 877,686 | 25 | 877,661 |
| APT / Gamaredon | 453,915 | 366,312 | 6 | 366,306 |
| APT / Higaisa | 609,394 | 533,596 | 0 | 533,596 |
| APT / Patchwork | 163,487 | 124,518 | 7 | 124,511 |

CHT 合計 314,980 筆事件，其中 Registry 218,533 筆、攻擊 690 筆（約 0.316%）。APT 合計 3,406,233 筆事件，其中 Registry 2,673,929 筆、攻擊 38 筆（約 0.00142%）。全部數字為原始事件筆數，尚未合併等價事件。

**這些數字改變實驗優先級：初版應採固定模型的零樣本／KG 檢索對照，不適合以 APT 38 個 Registry positive 作充分監督微調資料。** CHT 的 690 個 positive 中，546 個來自單一錄製；必須同時看錄製等權結果與個案差異。

額外稽核結果：

- 六個 CHT 錄製的 Registry 事件皆沒有 `dstNode.Value`。APT 有部分 Value，主跨域實驗需使用共同可用欄位；數值資料只作 APT 次要消融。
- CHT 的 `timestamp_raw` 恰只出現在所有非 benign 標註事件，必須排除欄位本身及其存在旗標。不能藉由它產生新的模型可見排序/缺值旗標。
- CobaltGroup 與 Higaisa 共享 46,748 個事件簽章；Gamaredon 與 Higaisa 共享 92,692 個。簽章包含事件內容、timestamp、UUID，排除 label／timestamp_raw，按每錄製內唯一簽章計數。
- APT 各錄製內有大量完全相同的 JSON 事件。相同粗粒度排序值下的相同事件不一定是錯誤重複，主結果保留原權重，另報等價事件群組敏感度。
- Patchwork 的 notebook checkpoint 與主 events.json SHA-256 完全相同，只納入主檔。
- APT 有 null 目的節點；所有11檔原始 timestamp 均未出現相鄰倒退，但 APT 大量同值，只能作 partial order。

檔案差異與處理規則：

- CHT 是 JSON array；APT 的 `events.json` 是 JSONL。只讀明確清單的 11 個錄製；排除 `.ipynb_checkpoints`。
- 每筆通常含 `srcNode`、`dstNode`、`relation`、`timestamp`、`label`；部分節點可為 null，不能直接當完整圖邊解析。
- `dstNode.Type=Registry` 是初版目標事件的選擇規則；其餘 Process／File／Network 事件可以提供歷史上下文，但不混進 Registry 目標的分母。
- `label=benign` 映射為 0；實際出現且通過白名單核對的 `Txxxx[.xxx]` 或 `Txxxx[.xxx]_<suffix>` 標籤映射為 1。將 technique 前綴與情境/步驟 suffix 分開保存，`_Linked` 也保留原值；不自行斷言 suffix 全是 Caldera ability ID。未標、未知、衝突標籤進隔離區，不能默認 benign。
- 程序路徑含 `Evil`、`MaliciousFiles`、樣本 hash 等實驗資訊；這些可能成為捷徑。`timestamp_raw` 等標註階段欄位也不進模型。
- `Key` 可能是完整 key，也可能串接 value name。`Value` 表示所附資料，不應直接假設為 value 名稱、資料型別、舊值或操作成功證據。
- 初步統計的「raw target 與 KG 節點完全相同」只作詞法檢查，尚未拆 key/value、處理 view 或套用候選模板，不能當成最終 KG 語意覆蓋率。

## 3. 資料適配、保留欄位與防洩漏

實作 `experiments/registry/ingest.py` 與 `normalize.py`，輸出一份 canonical JSONL 或 Parquet。建議 schema：

```json
{
  "event_id": "recording_sha256:source_row_index",
  "recording_id": "internal_group_id",
  "source_row_index": 123,
  "order_reference": 123,
  "actor_id": "recording_scoped_uuid",
  "relation": "RegSetValue",
  "raw_target": "original unchanged target",
  "key_path": null,
  "value_name": null,
  "value_data": null,
  "boundary_status": "unresolved",
  "operation_result": "not_recorded",
  "label_binary": 1,
  "label_original": "T1547.001"
}
```

標籤、來源檔名、錄製/APT 名稱與全域識別碼留在內部資料，不出現在 prompt。模型採欄位白名單，重建 event view，而非把原始 JSON 刪掉 label 就直接送入。

匿名化應保持行為語意：替換錄製樣本 hash、實驗命名的目錄、帳號與主機識別字串，對同一錄製中的相同實體使用一致代號；保留 HKLM/HKCU、System32、Run、服務/使用者路徑類別、參數結構與可疑操作本身。原始欄位在本機獨立保存；不能用檔名或標籤決定某個事件的匿名化方式。清理前後的差異另做敏感度分析。

key/value 拆解先建立 `relation_contract.json`：核對 RegQueryValue、RegSetValue、RegDeleteValue、RegOpenKey、RegCreateKey 等實際輸出規則。對已確認的 value operation 才可按該錄製格式拆出尾段；有反斜線的 value name、預設值或不確定欄位保留 unresolved。以有明確標註/原始匯出規格的範例測試，不靠尾段名稱猜測。

不得自動把 HKCR 當成 HKLM\\Software\\Classes，也不得移除 WOW6432Node。可使用現有明示 NT native adapter 與受限候選模板；精確匹配、模板候選、僅祖先命中、未知必須分開。

## 4. 標籤單位與上下文

**主標籤是當前 Registry 事件的人工標註。** 不把某程序有一筆攻擊事件就擴散成整個程序、錄製或所有視窗皆惡意。

用 `recording_id + process UUID` 隔離程序；PID 只能作輔助，不能跨錄製 join。排序先稽核原始列序與 order reference：嚴格較小的 order reference 可當歷史，同值視為順序未知；沒有可信 tie-breaker 時不把同值事件當前因。原始列號只用於可重現識別，不能假稱是實際時間先後。

主跨來源比較使用共同欄位，不要求 CHT 不存在的 Value data。APT 的 value-data 擴充另成消融，避免把來源的欄位差異與 KG 效果混合。

第一輪比較 K=0 與 K=16 筆**嚴格在目標之前**的同程序相關事件，保留 Registry／File／Process／Network 類型。K=8/32 是後續 sensitivity，不能使用測試成績選 K。程序父子關聯只有資料明確提供且發生在目標以前才使用；沒有就留空。

壓縮連續重複事件時保留 `repeat_count`、原始 row IDs 與排序範圍。不能壓縮跨程序、跨錄製或含衝突人工標籤的事件。標籤不作特徵，也不參與挑選「有利」的歷史上下文。主結果保留事件權重，另報重複群組等權的穩健性結果，避免大量重複讀取主導分數。

## 5. 切分：固定模型主評估，另設開發／外部測試路線

先做 `overlap_audit`，查完整事件、去環境識別資訊後的近似事件、程序身分、背景模板與共同錄製來源。相同 VM 或同一段背景錄製的重用可能造成洩漏；僅按檔名切分不充分。

實測重疊形成至少三個 APT 群組：`{CobaltGroup, Higaisa, Gamaredon}`、`{APT28}`、`{Patchwork}`。這是最小已知依賴分組，仍需查共同主機與再現腳本，不能視為證實各組獨立。三組的 Registry positive 分別為 31／0／7，因此不規劃把五個 APT 當五個獨立且雙類充分的訓練 folds。

**推薦第一輪主實驗：固定模型、固定 prompt/threshold、不以這11份資料做分類微調；分別在11份錄製跑配對消融。** 使用既有合成教學題測 parser/格式，不根據真實測試結果選提示。這輪是有人工標註的回溯研究，提供 KG 支援是否有用的初步證據；不宣稱模型跨來源訓練泛化。

若需要調參／few-shot，使用獨立的第二套設定：在 APT 三個依賴群組之間做有限開發，所有方法共用切分；接受單類 fold 僅能衡量 FPR。選定後凍結模型、KG、prompt、threshold、K 和程式，再對六個 CHT 錄製作跨來源測試。APT positive 太少時只測固定推論與門檻，不強行做 LoRA。不能把第一輪已看過的 CHT 成績用來選第二輪方法，再稱其為未見外部測試；若已檢視，須新增獨立錄製驗證。

正式任務的每個開發、驗證、測試資料路徑都寫入 `split_manifest.json`；禁止隨機逐列 8:1:1。CHT 在本階段已做結構與標籤數量盤點，測試的凍結邊界必須如實記錄。

反向 CHT→APT、混合域訓練以及 CHT 留一錄製實驗可作獨立次要研究，不與主實驗共用「最後測試」宣稱。每個 APT 目前只有一份錄製，因此外層分數只能支持這些再現情境的遷移，不能直接證明對整個 APT 家族或新組織泛化。

## 6. 固定模型與比較條件

先選一個可在現有硬體穩定執行的 3B–8B instruction SLM，凍結權重 revision、tokenizer、量化、context 長度及 decoding。先完成不微調的對照，再視結果增加第二個模型或 LoRA；本規劃不預設下載或付費 API。

| 條件 | 輸入 | 用途 |
|---|---|---|
| A raw | 去識別的原始事件欄位＋相同歷史 | 基準 |
| B normalized | A＋標準化操作、key/value 結構 | 量化適配與正規化收益 |
| C text | B＋相同命中節點的功能文字 | 量化一般文字知識收益 |
| D graph | B＋分層功能、scope、適用性、限制與相關語意邊 | 主要方法 |
| E unrelated | B＋等預算、與目標無關的知識 | 排除單純多文字效應 |

C/D 使用相同節點候選，分開紀錄 token 與截斷。D 比 C 有差異仍可能來自較豐富欄位；增加一個 D-flat（完全相同事實、去除階層與關係標示）才能主張結構表達本身的作用。E 的無關選擇與標籤無關，且報告其干擾性，不能只靠 E 變差證明 KG 有效。

輸出固定為 `prediction`、`score`（可取得時）、`evidence_event_ids`、`knowledge_node_ids`、簡短理由與 `unknowns`。理由不要求內部思考鏈。自報 confidence 不當作已校準機率；若拿不到可靠分數，僅報離散分類指標，不虛構 AUPRC。

不允許 prompt 包含既有標籤、APT/樣本名稱、ATT&CK 答案或測試樣本查詢結果。不能把原始私有 log 發送到外部服務作為實作預設。

## 7. 成本控制與執行分兩輪

第一輪：完整資料清點與 KG 命中稽核，採 label-independent cache。只對不同 `(key, value_name, view, graph_hash, adapter_version, template_mode)` 查詢一次 KG；事件推論仍保留各自歷史上下文。候選檢索／壓縮程式不能看到 label。

工程 smoke test 優先使用合成 fixture；若用真實事件測 prompt，該錄製／依賴群組必須列為開發資料。固定設定的 pilot 可納入所有人工攻擊目標，加每錄製至多 2,000 筆均勻隨機 benign，固定 seed 並記錄抽樣機率。依目前 raw 計數是 728 個 positive，加至多 22,000 個 negative；實際依去重/群組策略與單檔可用數量重算。硬負例另成 challenge set，不混成自然分布測試。先用 200 筆測得吞吐與 token 成本，再決定完整預算；資料條數不能直接等同實際推論時間。

先做 A/B/C/D、K=0；再做 A/D、K=16，避免把「加上下文」與「加 KG」混在同一比較。E、D-flat 與第二個模型待流程穩定後加入。這些是開發優先級，完整論文若宣稱圖結構收益必須包含對應消融。

完整測試優先保留所有事件與自然比例。若算力限制使 benign 必須抽樣，保留所有 positive、抽取隨機 negative 並記錄 inclusion probability；每類 recall 用相應機率加權估計，再計算 balanced accuracy。Precision、F1、AUPRC 會受盛行率影響，須用抽樣權重或標為抽樣分布結果，不能當真實部署數字。測試抽樣不能按 KG 命中與否篩掉困難案例。

## 8. 指標與統計

主要指標：`balanced_accuracy = (TPR + TNR)/2`，也就是兩類 recall 的 macro average。搭配 macro-F1、惡意 recall/precision、FPR、混淆矩陣、拒答/格式錯誤率、輸入 tokens 和每筆推論延遲。延遲使用實際實驗計時，與錄製 timestamp 無關。

資料不平衡仍會影響估計的不確定性；balanced accuracy 不會讓兩個 positive 變成可靠的大樣本。每個錄製各報正負 support、指標與錯誤數，再報錄製等權 macro 和 pooled 結果。只有 benign 的 Registry 子集：TPR/BA 標 N/A，只報 specificity/FPR，不能把單一類別的完美預測當成 100% binary BA。

方法差異採相同事件的 paired 比較。以錄製或相關程序區塊重抽樣估計差異區間，避免把數十萬相依事件當獨立樣本；只有五/六個錄製時，完整呈現逐錄製差異與不穩定性。依 technique 分組報告漏報率時，稀少標籤只作描述。

拒答與無效輸出不移出主測試分母：主結果以無法給出正確分類計為失敗，另報 coverage 和僅已判定子集的 selective 結果。預先固定重試政策、輸出驗證與門檻，不能對測試錯誤單獨重試。

## 9. 模組、產物與驗收

下列路徑為**待實作規格**，不是本次已執行的模型結果。

| 階段 | 實作內容 | 產物 | 驗收 |
|---|---|---|---|
| P0 資料契約 | 11檔白名單、hash、標籤映射、排序與欄位核對 | `source_manifest.json`、`label_map.json`、`relation_contract.json`、`annotation_audit.csv` | 解析成功、逐檔筆數守恆、未知隔離、排除 checkpoint |
| P1 適配 | key/value 拆分、view 保留、識別資訊匿名化 | `events.jsonl`、`normalization_audit.json`、`redaction_audit.json` | 原始可追溯；模型輸入無 label/來源答案；不猜測 outcome |
| P2 切分與上下文 | 重疊稽核、群組fold、前K筆 | `overlap_audit.json`、`split_manifest.json`、`targets.jsonl`、`contexts.jsonl` | 無跨split來源群組；無未來事件；保持目標原標籤 |
| P3 KG 表達 | 快取、精確/模板/祖先/未知區分、預算控制 | `kg_context_cache.jsonl`、`coverage_report.csv`、`prompts/*.jsonl` | 同資料同設定同輸出；來源/限制可追溯；未知不假裝命中 |
| P4 模型runner | resume、固定revision、統一輸出與重試 | `runs/<run_id>/config.json`、`predictions.jsonl`、`usage.json` | 每目標有結果或明示失敗；所有比較使用同一目標清單 |
| P5 評分與分析 | BA/F1/FPR、逐錄製與覆蓋分層、paired差異 | `metrics.json`、`per_recording.csv`、`confusion_matrices.csv`、`paired_deltas.csv`、`error_cases.jsonl` | 可由prediction重算；單類BA=N/A；分母與權重透明 |
| P6 教授討論 | 研究問題、實驗設計、正反案例、限制 | `EXPERIMENT_REPORT.md`、獨立圖表、精簡展示 | 主張逐一對應結果；失敗案例與負面結果完整保留 |

建議新增 `experiments/registry/{ingest,normalize,context,split,semantic,runner,metrics}.py` 與相應測試。所有衍生檔置於 `artifacts/registry-experiments/<dataset_version>/`，保留資料/KG/模型/設定 hash；不覆蓋原始 data 或既有 vault。使用 JSONL 便於串流，必要時額外匯出 Parquet；研究核心不必新增服務依賴。

## 10. 最先實作的範圍

優先完成 P0–P3：可靠的事件契約、群組切分、無洩漏上下文及 KG 覆蓋報告。確認缺失的 key/value 或 view 不會讓主要攻擊目標全部退化為 hive-only 說明後，再開始 SLM pilot。

若覆蓋不足，先報凍結 KG 的原始結果；任何用測試錄製啟發的新增知識只能進後續版本，不能回頭宣稱為未見測試的改善。第一輪論文主張限於目前資料與固定功能 KG 支援的事件判別；大規模真實部署、新 APT 家族與因果攻擊鏈需另外的證據。

方法參考：[balanced accuracy 定義](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.balanced_accuracy_score.html)；[LeaveOneGroupOut](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.LeaveOneGroupOut.html)。
