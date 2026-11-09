# 兩個研究方向的版本與進度管理

更新日期：2026-11-09。

| 研究 | 開發分支 | 獨立進度 |
|---|---|---|
| Registry 知識輔助逐事件判別與 SLM agent | `ANTS_KGmaer` | [KGmaer 進度](ANTS_KGmaer.md) |
| Registry 子圖擷取、檢索、切圖與分類 | `ANTS_KGraphier` | [KGraphier 進度](ANTS_KGraphier.md) |

兩個分支從目前 `forerunner/SLM_framework` 的共同基礎建立，保留既有程式與歷史。`ANTS_KGraphier` 另納入本機既有的 KGraphier 程式、設定、測試及 Markdown 報告。分支控制整個 repository，不會自動只追蹤同名目錄。後續提交請明確指定檔案，研究進度更新到對應文件。

## 日常操作

切換前先執行 `git status --short`，將目前題目的修改提交至該分支；未提交的變更可能跟著切換，不能用分支名稱隔離未提交檔案。

```bash
git switch ANTS_KGmaer
# 修改並檢查指定檔案後：
git add ANTS_KGmaer/ docs/research/ANTS_KGmaer.md
git diff --cached --stat
git commit -m "Record KGmaer experiment progress"
```

KGraphier 使用 `git switch ANTS_KGraphier`，並指定 `ANTS_KGraphier/` 與 `docs/research/ANTS_KGraphier.md`。共用知識或工具修改應獨立成一個 commit，再用 `git cherry-pick <commit>` 套用至另一分支，避免整條分支合併造成無關研究修改混入。

首次建立 GitHub 遠端分支時執行以下指令；本次整理僅建立本機分支，未執行推送：

```bash
git push -u origin ANTS_KGmaer
git push -u origin ANTS_KGraphier
```

## 版控邊界

- 追蹤：程式、測試、研究設定、來源清單與 checksum、知識 catalog／KG snapshot、合成測試案例、Markdown 進度與摘要。來源清單是重現用 metadata，不包含資料集內容。
- 本機保留：虛擬環境、原始／外部資料集、SQLite、下載的 vendor、模型權重、runs、workspaces、大型衍生資料與含事件追溯的詳細 JSON 報告。
- 根目錄的 `data/` 被忽略；`ANTS_KGmaer/ants_kgmaer/data/` 和 `ANTS_KGraphier/ants_kgraphier/classification/data.py` 是程式，必須追蹤。
- `artifacts/model-data/`、`artifacts/registry-inventory/`、`artifacts/experiment-planning/data_profile.json` 停止追蹤，檔案保留本機。新 checkout 需要取得授權資料並依原文件重建；依賴這些檔案的驗證不能假設它們已隨 clone 取得。
- `evaluation/` 是原有的合成教學案例與評分規準，保留版控；真實評估資料請放在忽略的資料目錄。

`.gitignore` 不會清除既有提交歷史。本次不重寫歷史，過去已提交或推送的衍生資料仍存在舊 commit；推送新分支也會帶上其祖先歷史。本設定防止後續誤加入指定路徑，不代表已完成歷史資料清除。其他檔名或位置的資料在提交前仍需檢查。

## 每次實驗的進度紀錄

更新對應研究文件中的待辦與紀錄表。至少記錄日期、研究問題、執行程式的 commit SHA、資料版本／checksum、KG／模型版本、設定／seed、本機產物位置、結果摘要與限制。程式有未提交修改時需明示，不能只用 HEAD 宣稱可重現。

本文與初始進度內容依既有 README／驗收報告整理；整理工作沒有重新執行研究實驗，也不將既有通過紀錄當成本次驗證結果。
