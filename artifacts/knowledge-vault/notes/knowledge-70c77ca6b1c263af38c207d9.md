---
node_id: "knowledge:70c77ca6b1c263af38c207d9"
generated: true
---

# Explorer

## Full prefix

~~~text
HKCU\SOFTWARE\Policies\Microsoft\Windows\Explorer
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:70c77ca6b1c263af38c207d9`

## Hierarchy

Parent: [Windows](knowledge-43021d03261165f313b86e60.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;file&#95;explorer&#95;administrative&#95;policies

This Explorer key in Software&#92;Policies contains documented user File Explorer policies, including control of search-box suggestions and the location of default Library definitions. These settings affect interface behavior and managed configuration rather than storing a general record of files opened or searches performed. The path is distinct from the legacy Explorer key under Microsoft&#92;Windows&#92;CurrentVersion&#92;Policies, and individual values must be interpreted using their own mappings.

## Atomic claim

Stores user File Explorer policies in the Software&#92;Policies namespace.

Scope: **user**

## Meaning in system-level logs

Use the full path and value to distinguish this key from the legacy Explorer policy branch. For search-suggestion policy changes, correlate user/session and application context rather than interpreting the policy value as a search term.

### What the path cannot establish

- The key is not itself a record of a user search or file access.
- Policy-path presence does not establish that suggestions are disabled or that Library locations have changed.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **DisableSearchBoxSuggestions** (value): When the policy is enabled, File Explorer suppresses search-box suggestion popups and stops saving entered search-box data for reuse.

### Claim-level evidence

- **direct** — Microsoft documents search-box behavior and managed default Library definitions at this Explorer policy location.
  Section: DisableSearchBoxSuggestions; DefaultLibrariesLocation / descriptions and ADMX mappings.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablesearchboxsuggestions](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablesearchboxsuggestions>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#addsearchinternetlinkinstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#addsearchinternetlinkinstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#cleartilesonexit](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#cleartilesonexit>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#desktopappsfirstinappsview](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#desktopappsfirstinappsview>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#disableglobalsearchonappsview](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#disableglobalsearchonappsview>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#gotodesktoponsignin](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#gotodesktoponsignin>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearcheverywherelinkinstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearcheverywherelinkinstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenudownload](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenudownload>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenuhomegroup](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenuhomegroup>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenurecordedtv](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenurecordedtv>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenuvideos](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenuvideos>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouninstallfromstart](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouninstallfromstart>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#powerbuttonaction](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#powerbuttonaction>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showappsviewonstart](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showappsviewonstart>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showrunasdifferentuserinstart](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showrunasdifferentuserinstart>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showstartondisplaywithforegroundonwinkey](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showstartondisplaywithforegroundonwinkey>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#startpinappswheninstalled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#startpinappswheninstalled>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#defaultlibrarieslocation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#defaultlibrarieslocation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disableindexedlibraryexperience](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disableindexedlibraryexperience>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disableknownfolders](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disableknownfolders>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablesearchboxsuggestions](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablesearchboxsuggestions>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#explorerribbonstartsminimized](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#explorerribbonstartsminimized>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#hidecontentviewmodesnippets](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#hidecontentviewmodesnippets>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nosearchinternettryharderbutton](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nosearchinternettryharderbutton>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#tryharderpinnedlibrary](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#tryharderpinnedlibrary>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#tryharderpinnedopensearch](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#tryharderpinnedopensearch>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
