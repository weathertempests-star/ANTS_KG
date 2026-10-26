---
node_id: "knowledge:754e0d5a736538dbdaa615d0"
generated: true
---

# Explorer

## Full prefix

~~~text
HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:754e0d5a736538dbdaa615d0`

## Hierarchy

Parent: [Policies](knowledge-0c0778e8b36d2e9810ea000d.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;explorer&#95;and&#95;shell&#95;policy&#95;settings

This Explorer key stores user-scoped Windows shell policies under the legacy CurrentVersion&#92;Policies branch. Documented settings include ignoring the user’s legacy logon run list and run-once list, while additional shell policies use the same container. These settings govern how consumers process configuration; the key is not itself the ordinary Run or RunOnce command-registration location. The exact policy value determines the behavior and relevant precedence rules.

## Atomic claim

Stores user Explorer and related shell policies, including legacy logon-list controls.

Scope: **user**

## Meaning in system-level logs

Retain the value name and data to distinguish a logon-list policy from other shell controls. Correlate policy results and subsequent process telemetry before concluding that a configured command was suppressed or executed.

### What the path cannot establish

- The Explorer key does not itself contain the ordinary Run command registration list.
- Key presence does not prove any logon program ran, was blocked, or was malicious.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **DisableCurrentUserRun** (value): User policy controlling whether the legacy customized run list is ignored; effective interpretation requires data and applicable machine policy.
- **DisableCurrentUserRunOnce** (value): User policy controlling whether the customized run-once list is ignored.

### Claim-level evidence

- **direct** — The user values DisableCurrentUserRun and DisableCurrentUserRunOnce control processing of legacy lists; the text documents computer-policy precedence.
  Section: DisableExplorerRunLegacy&#95;1; DisableExplorerRunOnceLegacy&#95;1 / descriptions and ADMX mappings.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **HAS_USER_POLICY_COUNTERPART** (incoming): [Explorer](knowledge-f07cdc68b92830b299c967c3.md)
  The legacy run-list policy has both machine and user forms; Microsoft states machine configuration takes precedence when both are configured. This precedence statement is specific to the documented setting, not every Explorer policy.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy_2>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunoncelegacy&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunoncelegacy_1>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunoncelegacy&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunoncelegacy_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#nowelcometips&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#nowelcometips_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#run&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#run_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nodeleteprinter](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nodeleteprinter>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disallowapps](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disallowapps>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#restrictapps](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#restrictapps>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#clearrecentdocsonexit](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#clearrecentdocsonexit>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#clearrecentprogfornewuserinstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#clearrecentprogfornewuserinstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#forcestartmenulogoff](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#forcestartmenulogoff>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#greymsiads](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#greymsiads>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#intellimenus](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#intellimenus>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#locktaskbar](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#locktaskbar>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#memcheckboxinrundlg](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#memcheckboxinrundlg>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#noautotraynotify](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#noautotraynotify>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#noballoontip](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#noballoontip>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nochangestartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nochangestartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#noclose](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#noclose>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nocommongroups](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nocommongroups>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nofavoritesmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nofavoritesmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nofind](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nofind>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nogamesfolderonstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nogamesfolderonstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nohelp](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nohelp>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#noinstrumentation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#noinstrumentation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nomoreprogramslist](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nomoreprogramslist>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nonetanddialupconnect](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nonetanddialupconnect>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nopinnedprograms](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nopinnedprograms>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#norecentdocsmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#norecentdocsmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#noresolvesearch](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#noresolvesearch>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#noresolvetrack](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#noresolvetrack>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#norun](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#norun>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearchcomminstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearchcomminstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearchcomputerlinkinstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearchcomputerlinkinstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearchfilesinstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearchfilesinstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearchinternetinstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearchinternetinstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearchprogramsinstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearchprogramsinstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosetfolders](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosetfolders>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosettaskbar](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosettaskbar>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosmconfigureprograms](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosmconfigureprograms>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosmmydocuments](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosmmydocuments>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosmmymusic](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosmmymusic>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosmmynetworkplaces](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosmmynetworkplaces>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosmmypictures](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosmmypictures>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenusubfolders](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenusubfolders>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartpage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartpage>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#notaskbarclock](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#notaskbarclock>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#notaskgrouping](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#notaskgrouping>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#notoolbarsontaskbar](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#notoolbarsontaskbar>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#notraycontextmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#notraycontextmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#notrayitemsdisplay](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#notrayitemsdisplay>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouserfolderonstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouserfolderonstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nousernameonstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nousernameonstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nowindowsupdate](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nowindowsupdate>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#quicklaunchenabled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#quicklaunchenabled>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#removeundockpcbutton](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#removeundockpcbutton>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showruninstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showruninstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#startmenulogoff](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#startmenulogoff>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#classicshell](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#classicshell>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#confirmfiledelete](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#confirmfiledelete>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablebinddirectlytopropertysetstorage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablebinddirectlytopropertysetstorage>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enforceshellextensionsecurity](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enforceshellextensionsecurity>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#linkresolveignorelinkinfo](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#linkresolveignorelinkinfo>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#maxrecentdocs](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#maxrecentdocs>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nocachethumbnailpictures](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nocachethumbnailpictures>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nocdburning](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nocdburning>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nochangeanimation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nochangeanimation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nochangekeyboardnavigationindicators](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nochangekeyboardnavigationindicators>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nodfstab](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nodfstab>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nodrives](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nodrives>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofilemenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofilemenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofolderoptions](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofolderoptions>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nohardwaretab](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nohardwaretab>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nomanagemycomputerverb](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nomanagemycomputerverb>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nomycomputershareddocuments](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nomycomputershareddocuments>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nonetconnectdisconnect](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nonetconnectdisconnect>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#norecyclefiles](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#norecyclefiles>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#norunasinstallprompt](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#norunasinstallprompt>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nosecuritytab](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nosecuritytab>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noshellsearchbutton](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noshellsearchbutton>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nostrcmplogical](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nostrcmplogical>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noviewcontextmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noviewcontextmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noviewondrive](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noviewondrive>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nowindowshotkeys](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nowindowshotkeys>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noworkgroupcontents](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noworkgroupcontents>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#promptrunasinstallnetpath](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#promptrunasinstallnetpath>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#recyclebinsize](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#recyclebinsize>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#shellprotocolprotectedmodetitle&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#shellprotocolprotectedmodetitle_1>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
