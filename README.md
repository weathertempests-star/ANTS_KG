# Registry 階層共用知識 Vault

這個專案把已有的 Registry inventory 與人工維護的英文功能說明合併，建立 **197 個共用知識節點、192 條父子邊**。全部 197 個節點已補英文功能知識：145 個有直接文件支持，52 個以 `structural` 明示由已記錄的子層推論其結構角色。另有 **46 條有說明與來源的語意關聯**，與父子邊分開。原有 7 份解釋及 ID 保留。

入口是 [Vault 索引](artifacts/knowledge-vault/INDEX.md)、[待補清單](artifacts/knowledge-vault/REVIEW_QUEUE.md)、[概念關聯](artifacts/knowledge-vault/CONCEPTS.md) 與 [完整 snapshot](artifacts/knowledge-vault/kg.json)。每個完整前綴只有一份知識；實際 audit input 只查詢這份圖，不產生事件節點，也不複製知識。

## 建置、查詢與驗證

使用 Python 3.9+，執行期只需標準函式庫。從 repository root 執行：

```bash
python -m standardizer_pkg knowledge-build knowledge/windows_registry.json \
  --inventory artifacts/registry-inventory/inventory.json \
  -o /tmp/registry-knowledge.json

python -m standardizer_pkg knowledge-vault /tmp/registry-knowledge.json \
  -o artifacts/knowledge-vault

python -m standardizer_pkg knowledge-validate-vault artifacts/knowledge-vault

python -m standardizer_pkg knowledge-resolve artifacts/knowledge-vault/kg.json registry \
  'HKLM\System\CurrentControlSet\Control\Session Manager'

python -m standardizer_pkg knowledge-context artifacts/knowledge-vault/kg.json \
  '\Registry\Machine\SYSTEM\CurrentControlSet\Services\ExampleSvc\Parameters' \
  --path-format nt_native --template-candidates
```

建圖輸出先寫到獨立 snapshot，再以 `knowledge-vault` 刷新。不要直接覆寫 vault 裡的 `kg.json`。`knowledge-build --markdown PATH` 可額外產生單檔預覽；省略 `--inventory` 時只建立 catalog 明確定義的節點，每個父節點都必須已定義。

CLI 提供上述四個建置／查詢／驗證命令，以及 `knowledge-context`、`knowledge-model-data`、`knowledge-validate-model-data`。安裝套件後也可使用 `ants-kg` 執行相同命令。模型使用方式、資料卡及評估方法見 [Registry learning guide](docs/REGISTRY_LEARNING_DATA.md)。

## 資料流程與來源邊界

```text
Registry inventory（完整路徑、階層、路徑證據）
  + knowledge/windows_registry.json（經來源研究與交叉審查的英文功能解釋）
  → Shared Knowledge JSON
  → 197 篇筆記 + INDEX + CONCEPTS + REVIEW_QUEUE + manifest
```

節點身分延續 `domain + 完整 canonical prefix`，7 個既有節點的 ID 保持不變。大小寫及 hive 縮寫會對齊；不同位置的同名 key 不會合併。Registry 的 `/` 是合法名稱字元，不當作反斜線分隔符。

snapshot schema 為 `prefix-knowledge-3`，保留 `id`、`domain`、`path`、`label`、`canonical_components`、`parent_id`、`role`、`explanation`、`status`，並增加：

| 欄位 | 意義 |
|---|---|
| `depth` | L1 為 hive／邏輯 root。 |
| `path_sources` | inventory 中該路徑或其後代的路徑證據；不自動支持功能說明。 |
| `explanation_sources` | catalog 中支持功能說明或明示結構推論的來源。 |
| `explicitly_listed` | 該前綴是否在 inventory 接受的路徑中明列，而非只有祖先推導。 |
| `is_placeholder` | 這一層本身是否為 `<ServiceName>` 等 placeholder。 |
| `template_dependent` | 完整前綴是否包含 placeholder，包括其固定名稱子層。 |
| `candidate_tags` | 本批固定為 `[]`，沒有執行 tagging。 |
| `research` | 原子主張、scope、log context、不可推論事項、值／子鍵範例、適用性及逐項證據。 |

`provenance` 保存建圖時 catalog 與 inventory 檔案的 SHA-256。inventory 的原始證據、隔離項目與來源讀取狀態仍各自保存；snapshot 的路徑來源不等於功能解釋來源。

原有 `prefix-knowledge-1` catalog 與 `prefix-knowledge-2` snapshot 仍可讀取；未提供研究擴充的一般建置保留 schema 2。新版 catalog 帶有 `research` 及獨立的 `relations`，來源欄位仍與 inventory 路徑證據分開。

本次依 roots／核心機制、使用者與安全區域、機器政策分為 74／63／60 個節點，由三個 agent 研究，另行交叉審查並由 root 整合。分工與模型設定見 [工作紀錄](knowledge/research/work_manifest.json)；[來源閱讀記錄](knowledge/research/source_reviews.json) 與 [審查報告](knowledge/research/reviews/) 可追溯具體修正。這是經 agent 審查的文件綜合，並非獨立人工標註。

後續修改於 `knowledge/research/batches/` 對應批次，連同來源閱讀記錄更新，再執行：

```bash
python scripts/assemble_registry_research.py
```

組裝會檢查 197 個精確路徑、來源閱讀覆蓋、必要研究欄位與重複主張，輸出 [catalog](knowledge/windows_registry.json)。接著使用前述命令重建 snapshot 與 Vault；模型資料也須同步重建。檢查通過代表結構與內容契約成立，事實正確性仍須閱讀來源與審查。

目前沒有 pending 節點。格式仍支援 `status="pending"`，其功能、角色與解釋來源必須留空，以便日後擴充時清楚表示未完成研究。52 個 structural 節點已有明示的結構說明與來源，不等同於直接證實某個實際功能或事件。

## 查詢的完整性

```python
from standardizer_pkg import KnowledgeBase

kb = KnowledgeBase.load("artifacts/knowledge-vault/kg.json")
result = kb.resolve(
    r"HKLM\System\CurrentControlSet\Control\Session Manager",
    "registry",
)
print(result["path_complete"], result["explanations_complete"])
for step in result["steps"]:
    print(step["raw"], step["explanation_status"], step["node_id"])
```

指定的 Session Manager input 仍命中 **5 個共用節點與 4 條邊**，兩種完整性均為 `true`。`explanations_complete` 表示沿途已有說明，仍須查看各節點是直接文件支持或結構推論；它不表示事件結果或實際政策生效。

- `path_complete`：所有輸入層都精確命中已收錄的前綴。
- `explanations_complete`：路徑完整，且沿途沒有待補功能說明。
- `complete`：等同 `explanations_complete`，避免把待補節點視為完整知識。
- 每層保留輸入原文、source span、node ID、說明狀態與知識副本。未知層是 `match="unknown"`、`node_id=null`、`knowledge=null`，不借用祖先的功能。

22 個模板分支節點（12 個 placeholder、10 個後代）已在圖中。預設查詢仍只做精確匹配；明示 `template_candidates=True`（CLI 為 `--template-candidates`）後，才以元件邊界及 SID、GUID、副檔名等型別限制檢索候選模板。具體名稱保存在 `template_bindings`；精確的 `path_complete` 仍為 `false`，候選鏈則由 `pattern_complete` 回報。候選只提供 schema 知識，不證明實際 key 存在、已載入或具有文件列出的值。字面上的 `<ServiceName>` 仍標示為 `literal_template`。所有查詢均唯讀。

## Vault 的刷新與一致性

| 路徑 | 內容 |
|---|---|
| `kg.json` | 完整 shared knowledge snapshot。 |
| `INDEX.md` | 從 hive 進入完整階層。 |
| `notes/knowledge-<ID>.md` | 穩定 ID 檔名，每節點一篇，含父子連結、完整前綴、層級、狀態與兩類來源。 |
| `REVIEW_QUEUE.md` | 依深度分組的待補清單；目前為 0。 |
| `CONCEPTS.md` | 46 條有來源的語意關聯及雙向筆記導覽。 |
| `manifest.json` | 匯出格式版本、snapshot schema、SHA-256 與每個產生檔案的校驗資訊。 |
| `personal/` | 使用者自行建立的個人筆記目錄，不由 exporter 管理。 |

JSON 與 Markdown 由同一份圖產生。驗證會從 JSON 重繪所有產生檔案，檢查精確內容、manifest、缺檔、額外的過期節點筆記及失效的內部連結；僅修改 manifest 的 hash 無法掩蓋 Markdown 差異。驗證是離線的一致性檢查，不會重新驗證外部文件內容，也不會自動把 catalog 的新修改納入既有 snapshot。

刷新前會驗證目前 vault，拒絕覆寫被手動修改、缺失或不一致的產生檔案。若已有手動研究內容，先把它保存到 `personal/`，再還原產生檔案或匯出到新目錄；沒有強制覆寫選項。有效刷新會移除新圖已不包含的舊節點筆記，保留個人目錄。寫入以單檔原子替換完成，manifest 最後寫入；刷新期間的讀者應等待完成再驗證。

## 範圍與後續研究

[CHT／Caldera 實驗實作計畫](docs/REGISTRY_EXPERIMENT_PLAN.md) 根據 `data/` 中 11 份錄製的全量盤點，定義事件標籤、順序上下文、洩漏排除、重疊群組切分、SLM 對照與預期產物。這是規劃與資料稽核，尚未執行模型實驗；統計見 [data profile](artifacts/experiment-planning/data_profile.json)，設定草案見 [protocol draft](artifacts/experiment-planning/protocol_draft.json)。

[SLM Agent 框架規劃](docs/SLM_AGENT_FRAMEWORK_PLAN.md) 定義單一 SLM、唯讀 KG 工具、受限查詢循環、證據與答案隔離，以及固定流程／自主檢索的配對比較；[agent protocol draft](artifacts/experiment-planning/agent_protocol_draft.json) 保存初始預算與驗收條件。此框架尚未實作或執行模型推論。

[完整 inventory 說明](docs/REGISTRY_INVENTORY_PLAN.md) 保留來源、隔離理由、計數方法與覆蓋限制。這是跨版本文件清單，不是完整 Windows Registry 或特定主機的實例快照。逐層節點數為 **5、8、12、20、30、57、32、12、21**。

| 階段 | 層級 | 全部節點 | 待補解釋 |
|---|---|---:|---:|
| A | L1–L4 | 45 | 0 |
| B | L5–L7 | 119 | 0 |
| C | L8–L9 | 33 | 0 |

本次已完成範圍內的功能說明與來源，並提供逐層模型檢索、197 筆節點資料、394 筆指令範例及 17 個獨立保存的教學評估題。尚未訓練模型或宣稱效能提升；後續以實際版本化 log 評估，再研究功能標籤 taxonomy。未來候選標籤需要保存標籤、規則 ID、規則版本與命中依據；目前 schema 拒絕非空候選標籤，不把舊分類直接提升為功能。

[Registry 規則參考資料](knowledge/registry_rule_reference.json) 是不執行的研究封存，含原始 regex、flags、群組、順序、輸出標籤、fallback、來源位置、原始內容與 SHA-256。84 條表列規則中只有 hive 與 category 表由原入口使用；object、detail 表未被執行，另有 1 條註解停用規則。操作／風險暗示及未啟用狀態均另行標記，所有規則的功能標籤核准狀態都為 false。新版程式不讀取這份封存。

先用明確 Windows baseline 擴充覆蓋，再擴充 file 與 command。核心目前保留 Windows absolute drive file path 與 command token-prefix 的明確定義介面，但沒有附帶功能 catalog。Registry 只支援明示的 NT native `\Registry\Machine`／`\Registry\User` 轉換；不猜測 HKCU、remote alias、value 邊界或 WOW64 view。UNC、變數展開與完整 shell AST 尚不支援。`command_parser` 保留供現有查詢與後續 command 知識使用。

## 開發與驗證

核心程式為 `standardizer_pkg/knowledge.py`，vault exporter 為 `standardizer_pkg/zettelkasten.py`；公開 API 只有 `KnowledgeBase`、`export_vault`、`validate_vault`。

```bash
python -m unittest discover -s tests
python -m compileall -q standardizer_pkg scripts tests
python -m standardizer_pkg --help
python -m standardizer_pkg knowledge-validate-vault artifacts/knowledge-vault
python -m standardizer_pkg knowledge-validate-model-data artifacts/knowledge-vault/kg.json artifacts/model-data
python scripts/prepare_registry_evaluation.py --validate
python scripts/audit_registry_research.py --as-of 2026-10-25
```

重算 inventory 使用保留的觀察資料，不連網、不新增功能說明：

```bash
python scripts/plan_registry_inventory.py
```

清理採逐檔清單，檔名與刪除前 hash 保存在 [清理紀錄](artifacts/prototype-cleanup.json)。套件不再依賴 pandas。`AGENTS.md` 按要求保持原文；其中歷史結構與命令不代表目前介面，現行操作與開發說明以本 README 為準。
