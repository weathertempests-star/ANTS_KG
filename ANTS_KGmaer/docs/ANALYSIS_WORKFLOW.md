# 覆蓋、敏感度與人工審核

所有命令從 `ANTS_KGmaer` 執行。新分析使用新目錄／檔案，不覆蓋既有產物。下列工作在研究機器執行，Spark 只接收模型推論請求。

## 1. 在推論前盤點 KG 覆蓋

```bash
python -m ants_kgmaer prepare \
  --config configs/prepare-pilot.json \
  --dataset workspaces/recordings-v1 --selection workspaces/pilot-v1 \
  --output workspaces/pilot-prepared-v1
```

範例設定使用所有 pilot 目標、K=0、關閉模板候選，不呼叫模型。產出：

- `contexts.jsonl`：模型事件封包與外層追溯資訊。只有 `context` 能進模型，不可直接將整列傳入 prompt。
- `kg_context_cache.jsonl`、`kg_cache.sqlite`：不含答案的查詢結果與內容校驗。
- `coverage_events.jsonl`：逐目標匹配狀態、說明完整度、命中節點數與最深層級。
- `coverage_report.csv`：由獨立評估模組關聯人工答案後的逐錄製／類別／匹配狀態統計，不能回傳給模型。
- `config.json`、`manifest.json`：資料、選樣、KG、設定與程式身分及產物校驗。

`exact` 只表示完整路徑匹配，功能說明是否完整另看 `explanations_complete`。`ancestor`、`unknown`、`missing_target` 與 `boundary_unresolved` 均保留。模板候選只在明確啟用時產生，不能視為具體節點證實的語意。

本次已執行 22,330 個 pilot 目標：ancestor 11,704、boundary_unresolved 7,643、exact 2,905、unknown 78。728 個惡意標註事件中分別為 ancestor 21、boundary_unresolved 705、exact 2。這是**抽樣目標的未加權覆蓋計數**，不是完整 Registry 母體覆蓋或模型判別成績。705 個邊界不確定事件不能當成已確認末端 key/value 功能；若取得匯出格式證據，須更新欄位契約並建立新的資料版本。

完整母體的獨立覆蓋稽核不需要先匯出數百萬筆 context：

```bash
python -m ants_kgmaer coverage-population \
  --dataset workspaces/recordings-v1 --output workspaces/population-coverage-v1
```

此命令保留每個 Registry event 與查詢的 SQLite 對照，只對不同查詢取得一次 KG；完成後由獨立評估模組關聯人工答案，輸出 `coverage_report.csv`、`summary.json`。未知／隔離標籤也保留在完整母體計數，另列 quarantined。必須等 manifest.complete=true 才能使用母體結論；中斷的稽核目錄不能視為完成，也不支援直接 resume，應保留診斷後另建新目錄。

在評分時加入匹配分層：

```bash
python -m ants_kgmaer evaluate \
  --dataset workspaces/recordings-v1 --selection workspaces/pilot-v1 \
  --run runs/full-pilot-condition --prepared workspaces/pilot-prepared-v1 \
  --output runs/full-pilot-condition-evaluation
```

prepared 與 run 的資料、選樣、KG、模板政策、split 及工程目標上限須一致。20 筆工程 run 不能直接套用完整 pilot 的 prepared；以該工程設定另做 prepare。評分器會拒絕缺少、重複或多出的覆蓋列。

## 2. 重複群組敏感度

```bash
python -m ants_kgmaer duplicates \
  --dataset workspaces/recordings-v1 \
  --evaluation runs/full-pilot-condition-evaluation \
  --output runs/duplicate-sensitivity.json
```

分別以 exact 與 normalized 等價條件重新加權已評估事件。群組不跨錄製、不跨程序；normalized 另外要求排序值與可選 Value 資料相同。每個沒有標籤衝突的觀測群組權重總和為 1，群組內按原逆抽樣機率權重分配。含衝突標籤的群組保留各事件、各權重 1，不合併答案。

此結果是**已觀測抽樣群組敏感度**，不是所有母體群組的無偏估計。未抽中的成員仍可能帶有其他標籤衝突；輸出會保留此限制。主要逐事件結果不變，也不壓縮提供給模型的歷史。

評分另保留逐 technique 描述性分層。這些答案只存在 evaluator 產物，不能輸入模型；僅有惡意事件的 technique 子集 BA=N/A，應檢視 recall 與 support，不能將少量案例宣稱為穩定家族偵測能力。

## 3. 人工證據支持率

```bash
python -m ants_kgmaer review-export \
  --run runs/full-pilot-condition --limit 100 --seed 20261026 \
  --output runs/claim-review
```

從有最終證據的 valid／abstained 輸出主張中均勻抽樣。`blind/` 內提供待審主張及當時實際可見的事件／知識；`internal/` 保存原事件與主張索引的對照，不供審查者使用。封包隱藏人工答案、模型名稱、條件與分類結果，但主張措辭或證據形式仍可能讓人猜到條件，因此不宣稱完全盲化。

複製 `blind/reviews.csv` 到另一個檔案，例如 `runs/completed-reviews.csv`，由審查者填入：

| 欄位 | 內容 |
|---|---|
| review_id | 保持不變 |
| judgment | supported、unsupported、uncertain；未審留空 |
| reviewer | 審查者代號 |
| note | 簡短支持／不支持的依據 |

```bash
python -m ants_kgmaer review-import \
  --review runs/claim-review --annotations runs/completed-reviews.csv \
  --output runs/human-support.json
```

引用 ID 有效不等於主張獲得支持。輸出分開報告引用有效率、人工支持率、審查完成率及待審數。uncertain 保留在已審分母，pending 不算支持；沒有主張／沒有人完成審查時支持率是 null，不自動報 100%。不完整審查可能有選擇偏差。人工審核結果不回饋修改同一測試 run 的 prompt。

## 4. 成本與驗證限制

新 run 的 `usage.json` 彙整所有已完成目標的已知 token、未知用量上界、工具成功／拒絕／重複率、最終輸出驗證率、拒答與預算耗盡率。p50/p95 只涵蓋收到回覆的模型呼叫，不含失敗請求或 client overhead；mock 時間／tokens 不代表模型效能。Replay 取得證據成本另外列出。

目前可執行本地單元、資料與 mock 整合測試；此環境禁止建立 socket，兩項真正 loopback HTTP 測試會明示 skip，尚未驗證 Spark 實機。具備 socket 權限的研究機器可執行：

```bash
python -m unittest discover -s tests -p test_http_integration.py -v
```

該測試的 HTTP peer 仍是合成回覆，只驗證網路介面、認證及用量處理。LangGraph 選用後端與真實 Spark 模型仍有獨立驗收待辦；不能把 mock 或 HTTP fixture 當成模型研究結果。
