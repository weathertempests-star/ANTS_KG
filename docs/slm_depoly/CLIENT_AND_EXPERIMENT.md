# 內網 Client：API 驗證與研究整合

先完成 [Spark 部署](README.md)。本文件全部在 **內網研究機器** 執行，該機器可以是 x86，不需要 GPU 或 CUDA。KG、agent、人工標籤與原始資料保留在這裡。

## 1. 建立 API 驗證環境與取得 key

```bash
# [Client] 在 Ants-KG 根目錄
export SLM_CLIENT_STATE="$HOME/ants-slm-client/qwen35-27b-v1"
export SLM_BASE_URL="http://192.168.50.10:8000"
mkdir -p "$SLM_CLIENT_STATE"
chmod 700 "$SLM_CLIENT_STATE"
python3 -m venv "$SLM_CLIENT_STATE/venv"
"$SLM_CLIENT_STATE/venv/bin/python" -m pip install jsonschema
"$SLM_CLIENT_STATE/venv/bin/python" -m pip freeze > "$SLM_CLIENT_STATE/requirements.lock.txt"
scp spark-user@192.168.50.10:~/ants-slm/qwen35-27b-bf16-v1/api.key "$SLM_CLIENT_STATE/api.key"
chmod 600 "$SLM_CLIENT_STATE/api.key"
export SLM_API_KEY_FILE="$SLM_CLIENT_STATE/api.key"
```

API URL 的 `/v1` 只在實際 endpoint 或 SDK base URL 使用；附帶的 probe 接受不帶 `/v1` 的 origin。key 是實驗室此模型服務的憑證，不是雲端服務 key。不得將它加入資料集、prompt、trace 或 Git。

## 2. 執行三種合成請求

```bash
# [Client]
"$SLM_CLIENT_STATE/venv/bin/python" docs/slm_depoly/scripts/probe_server.py \
  --base-url "$SLM_BASE_URL" --allow-lan \
  --out "$SLM_CLIENT_STATE/probe-001"
```

腳本會確認 `/health`、`/v1/models`，然後測試：

| 檔案 | 驗證目的 |
|---|---|
| [01_text.json](requests/01_text.json) | API 能回傳非空、正常結束的文字 |
| [02_decision.json](requests/02_decision.json) | JSON schema、事件／知識引用、usage、輸出長度 |
| [03_action.json](requests/03_action.json) | 受約束的工具動作 JSON 能通過 schema |

產物是 `probe-001/probe.jsonl`，保存每個 request、response、usage、端到端延遲和失敗原因，不保存 Authorization header。既有檔案不覆寫。腳本禁用環境代理與 HTTP redirect，避免內網請求被轉送到其他位置；LAN 模式要求私有 IP 與 key。使用網域名稱的服務可先填寫其實際內網 IP，或經本機 SSH tunnel 測試。

**這些 probes 不評估惡意偵測準確率。** 工具 fixture 明確要求固定動作，只能驗證傳輸／格式，不證明 agent 會選對工具。decision fixture 也不以預測類別作正確率驗收，只有 schema／引用檢查。

若 status 為 error，先查看 JSONL；HTTP 401、finish_reason=length、無法解析 JSON、思考內容未停用、亂造引用，都不能被當作通過。

## 3. 最小 Python API 呼叫

此例使用標準函式庫，不需雲端 SDK。`response_format` 與 `chat_template_kwargs` 直接放在 HTTP JSON 根層；使用某些 SDK 時才需要其 `extra_body` 包裝。

```python
import json
import os
from pathlib import Path
from urllib.request import ProxyHandler, Request, build_opener

base = os.environ['SLM_BASE_URL'].rstrip('/')
key = Path(os.environ['SLM_API_KEY_FILE']).read_text().strip()
payload = json.loads(Path('docs/slm_depoly/requests/02_decision.json').read_text())
request = Request(
    base + '/v1/chat/completions',
    data=json.dumps(payload).encode(),
    headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key},
)
# 固定的可信內網端點；正式 adapter 另需沿用 probe 的 redirect／origin 檢查。
with build_opener(ProxyHandler({})).open(request, timeout=300) as response:
    result = json.load(response)
if result['choices'][0]['finish_reason'] != 'stop':
    raise RuntimeError('Incomplete generation; preserve as a failed attempt')
answer = json.loads(result['choices'][0]['message']['content'])
print(answer)
print(result['usage'])
```

所有同模型比較使用相同 decoding：本目錄初始值為 temperature=0.7、top_p=0.8、top_k=20、min_p=0、seed=20261026、max_tokens=512、thinking=false。這是工程起點；在開發階段凍結後才用於正式比較。固定 seed 不承諾跨 GPU／batch／引擎版本完全相同的結果。[Qwen3.5 non-thinking API 設定](https://huggingface.co/Qwen/Qwen3.5-27B)

JSON schema 約束是格式保證的一部分，仍需要 client 端驗證引用與語意支持。模型自報 confidence 不當作已校準機率。[vLLM structured outputs](https://docs.vllm.ai/en/v0.28.0/features/structured_outputs/)

## 4. Agent 與 KG 的邊界

```text
Client:
  選目標 → 適配／去識別 → 建構允許上下文
     ↓
  POST Spark /v1/chat/completions → 取得 action JSON
     ↓
  Client 驗證 action、event IDs、node IDs、預算
     ↓
  Client 執行 KnowledgeBase／先前事件查詢
     ↓
  將工具結果加入 evidence packet → 再 POST Spark
     ↓
  驗證最終判斷 → 保存 prediction → 獨立 evaluator 關聯 label
```

Spark 只回傳文字／JSON。它不持有 Registry KG，不掛載 log、不讀取 label、不執行模型提出的工具。服務端的 native tool calling 也只會產生工具請求，不代表工具已執行。

既有 [Agent 框架](../SLM_AGENT_FRAMEWORK_PLAN.md) 的狀態機、工具白名單、兩輪檢索／四次模型呼叫上限，仍由 Client 實作與約束。此次部署文件沒有新增完整 agent runner。

在 Client 驗證現有 KG 查詢：

```bash
# [Client] 在專案根目錄，使用可執行本專案的 Python
python3 -m standardizer_pkg knowledge-context \
  artifacts/knowledge-vault/kg.json \
  'HKLM\SYSTEM\CurrentControlSet\Control\Session Manager' \
  -o "$SLM_CLIENT_STATE/session-manager-context.json"
```

由固定 serializer 將該結果的功能、來源、scope、cannot_infer 與命中狀態放入證據封包；不要讓模型自行拆 key/value，或把完整原始 JSON log 直接當作 prompt。實驗用 serializer／事件 runner 仍依前述計畫實作。

## 5. 研究預算與服務容量分開

- Spark 的 8K 是輸入加輸出的容量上限。第一輪研究仍限制每次 input≤4096、output≤512，不能因換大模型就偷偷增加某一組證據量。
- Client 需在送出前，以固定 revision 的 tokenizer／chat template 計數，包含 system、歷史、工具結果及 schema 說明。可以從 Spark 的 model lock 找到 tokenizer revision，再於 Client 下載相同 tokenizer 小檔案；不需載入權重。
- 超長證據依固定規則裁切整個主張，並保存截斷紀錄；不直接裁掉 scope／限制。server 拒絕與輸出截斷皆保存為失敗。
- 本 probe 在回覆後檢查 usage；它不能取代正式 runner 的送出前 token-budget 檢查。
- 兩個同時執行序列不等於只能兩台 client 連線。Client 應設定共享的提交併發上限，先1、再2，記錄排隊延遲。
- 模型 API timeout 重送可能重複消耗推論；保留 attempt ID、已知 usage、未知用量，不能將超時當成零成本。

## 6. 正式實驗前的凍結清單

| Spark 端保存 | Client 端保存 |
|---|---|
| 模型 repo、commit、權重與 tokenizer hash | 資料版本、目標清單、群組切分 |
| image digest、vLLM／PyTorch／CUDA／driver 版本 | KG snapshot、工具契約、serializer／prompt hash |
| 精度、context、cache、併發、thinking 相關設定 | decoding、seed、token／呼叫上限、修復政策 |
| 服務啟動參數與維運時間 | request／response、引用、tokens、失敗與真實計時 |

人工標註維持逐事件目標；timestamp 僅作先後參考。同 timestamp 不猜順序。label、timestamp_raw、APT 名稱、樣本 hash 與實驗目錄提示，不能透過 API 洩漏到模型。

先以同模型比較固定 KG／agent，再比較27B與32B／122B；這能分離 KG、agent policy 與 backbone 的影響。`BA_all`、單類 N/A、拒答分母、逐錄製結果及依賴群組沿用 [原實驗計畫](../REGISTRY_EXPERIMENT_PLAN.md)，不因服務移到 Spark 而改變。
