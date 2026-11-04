# Windows Registry 清單與分層節點規劃

收集日期：2026-10-16。這是一份公開文件的跨版本 inventory，用來規劃 shared knowledge 的建置工作量；目前已據此建立 [197 節點 vault](../artifacts/knowledge-vault/INDEX.md)。它不是特定 Windows build 的 Registry dump，也不是完整 Windows Registry 清單。

## 收集結果

- 嘗試讀取 69 個 Microsoft Learn 文件來源，55 個取得內容，47 個提供了本次接受的路徑證據。其餘來源的讀取狀態保留在 source manifest；讀不到不代表該功能不存在。
- 取得 509 筆 ADMX policy-to-key mapping，以及 58 筆人工核對的結構路徑／模板，共 567 筆路徑證據。
- 21 筆證據涉及 10 條疑似格式錯誤路徑，隔離後接受 **141 條不重複的固定／模板路徑**。
- 展開祖先並共用完整前綴後，需要 **197 個知識節點、192 條父子邊**：175 個固定前綴節點、22 個依賴模板的節點。
- 22 個模板分支節點中，12 個本身是 placeholder；另外 10 個是 placeholder 下的固定名稱子層。它們是知識模式，不是 22 個實際 Registry instance。
- 原有的 7 個 Registry 知識節點都在此清單內；最初建置時另有 190 個 pending 節點。2026-10-21 的獨立功能研究已補全全部 197 個節點（145 documented、52 structural），既有七份解釋維持原文；本 inventory 仍僅提供路徑證據。

## 分層節點數量

L1 是 hive／邏輯 root。例如 `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager` 位於 L5。每一個不同的完整前綴是一個 node，不能只依最後一段名稱去重。

以下是**本次清單轉成 KG 的可重算建圖數量**，也是第一批工作的預估節點數；不是對完整 Windows Registry 的統計推估。

| 層級 | 固定前綴 | 模板分支 | 本層預估節點 |
|---|---:|---:|---:|
| L1 | 5 | 0 | 5 |
| L2 | 7 | 1 | 8 |
| L3 | 10 | 2 | 12 |
| L4 | 17 | 3 | 20 |
| L5 | 25 | 5 | 30 |
| L6 | 48 | 9 | 57 |
| L7 | 30 | 2 | 32 |
| L8 | 12 | 0 | 12 |
| L9 | 21 | 0 | 21 |
| **合計** | **175** | **22** | **197** |

按 root 分組：HKLM 138、HKCU 50、HKU 7、HKCR 1、HKCC 1。HKCR／HKCC 目前只收錄入口，分支覆蓋明顯不足，不能由這個比例推論 Windows 真實分布。

## 收集範圍與來源

1. 核心結構：HKLM 的 HARDWARE、SAM、SECURITY、SOFTWARE、SYSTEM；CurrentControlSet 下的 Control、Services、Enum、Hardware Profiles；Session Manager、LSA 與 NetworkProvider。
2. 政策分支：登入、檔案系統、事件記錄、DNS、網路連線、使用者設定檔、credential providers、裝置安裝、遠端桌面、SMB、列印、Explorer、Start menu、Kerberos、Netlogon、W32Time、AppCompat、DeviceGuard 等。
3. 軟體／使用者：Run、RunOnce、Uninstall、環境變數、COM CLSID／AppID／Interface／ProgID／副檔名與憑證儲存位置。

代表性來源：

- [Registry structure](https://learn.microsoft.com/en-us/windows/win32/sysinfo/structure-of-the-registry)
- [Predefined keys](https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys)
- [Control tree](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree)
- [Services tree](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree)
- [ADMX EventLog mapping](https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog)
- [COM CLSID](https://learn.microsoft.com/en-us/windows/win32/com/clsid-key-hklm)
- [Certificate store locations](https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations)

每條接受的路徑與每個祖先節點均保留來源 URL。ADMX 路徑的 hive 依 Location 欄位推導：Computer Configuration → HKLM，User Configuration → HKCU；原始相對 key、政策 section、來源行號及 value name 保存在 observation 中。值名稱不加入階層計數。抓取是有範圍的文件收集，不宣稱完整爬取所有 Microsoft 文件或所有政策。

## 動態層如何規劃

```text
HKLM
└── SYSTEM
    └── CurrentControlSet
        └── Services
            ├── <ServiceName>       # 共用的知識模板
            │   ├── Parameters
            │   ├── Performance
            │   └── NetworkProvider
            ├── EventLog            # 文件明確命名的服務路徑
            │   └── <LogName>
            └── Tcpip6
                └── Parameters
```

建議先為 `<ServiceName>` 寫「服務／驅動設定容器」的角色解釋，再對已知的具體服務補專屬知識。GUID、UserHive、ProductCode 同理。匹配時應保留 raw component，優先命中具體知識，否則匹配有型別及上下文限制的模板，且必須標示匹配種類。

模板中的 `<CLSID>` 是動態 slot；來源列出的特定 GUID 則是固定名稱，不能把所有 GUID 一律折疊。相同 `<ServiceName>` 在不同完整前綴下仍是不同知識節點。

目前 KnowledgeBase.resolve 預設仍只做精確查詢；明示啟用後，可依完整前綴與 SID／GUID／副檔名等元件限制，把具體名稱連到這 22 個模板分支節點。結果會分開回報 `path_complete` 與 `pattern_complete`，並保留 binding；候選模板不是實例存在、載入狀態或值內容的證據。若每個實際服務／使用者／裝置都具體展開，節點數取決於所選 Windows image 與安裝狀態，無法由這 47 份文件可靠估計。

令 P 為路徑清單，本次第 d 層數量為 `N_d = |{prefix(p,d): p in P, depth(p)>=d}|`。若日後具體化模板，要先代入實際名稱再對所有前綴取聯集；不能把每個模板數量簡單相乘，因為固定分支與模板展開結果可能重疊。

## 建置順序

| 階段 | 層級 | 本批節點數 | 工作重點 |
|---|---|---:|---|
| A | L1–L4 | 45 | 建立 namespace、machine/user scope、系統與軟體分支的英文角色說明。 |
| B | L5–L7 | 119 | 補 subsystem、service、policy、COM 等具體功能；審核模板與固定節點的邊界。 |
| C | L8–L9 | 33 | 深層 policy keys，確認 value 與 subkey、來源版本及固定編號的意義。 |

目前階層與範圍內功能研究已完成；A／B／C 階段待補數均為 0，見 [審核清單](../artifacts/knowledge-vault/REVIEW_QUEUE.md)。這是範圍內的知識補充順序，不代表所有 L5 節點都屬於相同語意抽象層。正式 schema 應同時保留 depth 與 semantic role。

## 尚未涵蓋與品質限制

- 清單偏向公開可設定的 policy keys。尚未充分涵蓋 Windows Update、TaskCache、完整使用者 Shell 設定、所有驅動／服務／裝置 instance、第三方軟體與未公開內部鍵。
- 文件可能同時描述舊版與新版 Windows 的可選設定；路徑可存在不等於每個 Windows 11／Server 安裝都預設存在。每個版本是否適用，後續需逐條確認來源 applicability。
- 這裡的五個 root 是常見 Registry namespace 規劃，不表示 Windows 只有五個 predefined handles。Performance 類 pseudo-keys 等不在本次範圍。
- HKCU 與 HKU 的使用者分支、HKCC 與 Hardware Profiles、HKCR 的合併視圖有別名／視圖關係。本次保留查詢入口，不將邏輯節點數稱為實體 hive 或實體 key 數。
- ADMX_RemovableStorage 文件的部分 `RemovableStorageDevices{GUID}` 缺少疑似應有的分隔符；保留於 inventory 的 quarantined 區，未自行修正或納入 197 個節點。
- TCP/IP 舊版文章標明 Windows XP，因此本次沒有拿它推定現代 Windows 的 IPv4 全部路徑。

若要估算「特定 Windows 系統的全部節點」，下一步應選定 client/server build、架構、安裝角色及初始映像，以**只列舉 key 名稱、不收集 value data**的方式取得 baseline，再與文件清單比較。這能分開計算觀察到的實例量、可共用的語意模板量與尚無解釋的路徑量；本次尚未取得或列舉實際 Windows 主機。

## 檔案與重算

- [完整路徑 CSV](../artifacts/registry-inventory/paths.csv)
- [展開後的 197 個節點 CSV](../artifacts/registry-inventory/nodes.csv)
- [逐層數量 CSV](../artifacts/registry-inventory/depth-counts.csv)
- [路徑、來源、隔離項目及統計 JSON](../artifacts/registry-inventory/inventory.json)
- [來源讀取狀態](../knowledge/registry_inventory_sources.json)
- [ADMX 路徑證據](../knowledge/registry_policy_observations.json)
- [核心結構路徑證據](../knowledge/registry_core_observations.json)

```bash
python scripts/plan_registry_inventory.py
python -m unittest discover -s tests
```

重算器使用已保存的路徑證據，不需網路；它重現統計，不會重新爬取文件，也不會新增正式知識說明。
