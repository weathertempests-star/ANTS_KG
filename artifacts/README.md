# 可重建的研究產物

- [Registry knowledge vault](knowledge-vault/INDEX.md)：197 個共用知識節點、192 條父子邊；197 份研究說明（145 documented、52 structural）、46 條獨立語意關聯；原 7 份解釋保留。
- [審核清單](knowledge-vault/REVIEW_QUEUE.md)：依深度分組的待補功能知識，目前為零。
- [Shared knowledge JSON](knowledge-vault/kg.json) 與 [一致性 manifest](knowledge-vault/manifest.json)：由同一份圖產生並驗證。
- [Registry inventory](registry-inventory/inventory.json)：原始路徑證據、來源、隔離項目與統計；其他 CSV 保留在同目錄。
- [逐檔清理紀錄](prototype-cleanup.json)：移除檔案的精確位置與刪除前 SHA-256。

重建與驗證命令見 [README](../README.md)。研究修改於 [catalog](../knowledge/windows_registry.json)，個人筆記放在 vault 的 `personal/` 目錄；不要直接修改產生檔案。原 Registry 規則的研究封存位於 [規則參考 JSON](../knowledge/registry_rule_reference.json)，不參與建圖或查詢。

- [概念關聯](knowledge-vault/CONCEPTS.md)：帶說明與來源的跨分支連結。
- [模型資料 manifest](model-data/manifest.json)：197 筆節點、394 筆指令範例、圖索引與完整來源；使用及拆分限制見 [資料卡](../docs/REGISTRY_LEARNING_DATA.md)。
- [評估題](../evaluation/registry_cases.jsonl)、[runner prompts](../evaluation/prompts.jsonl)、[scorer answer key](../evaluation/answer-key.jsonl) 與 [評分規準](../evaluation/rubric.json)：17 個合成教學案例，不是已觀測事件或已測得的模型結果；runner 與答案分離。
- [研究一致性稽核](../knowledge/research/research_audit.json)：重算 catalog、vault、model-data、評估封裝、審查覆蓋及來源閱讀時效。
