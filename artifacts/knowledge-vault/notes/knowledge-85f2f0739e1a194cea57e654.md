---
node_id: "knowledge:85f2f0739e1a194cea57e654"
generated: true
---

# CurrentVersion

## Full prefix

~~~text
HKCU\Software\Microsoft\Windows\CurrentVersion
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:85f2f0739e1a194cea57e654`

## Hierarchy

Parent: [Windows](knowledge-2f55e36525d8e2e6b07a950f.md)

Children:

- [Policies](knowledge-0c0778e8b36d2e9810ea000d.md)
- [Run](knowledge-133870b9f8825b6703ab5724.md)
- [RunOnce](knowledge-a59b3ac84eac68e574106e36.md)

## Functional explanation

Status: **structural**

Role: user&#95;windows&#95;version&#95;namespace

CurrentVersion is the shared parent of several documented Windows configuration locations in the current-user hive. In this inventory, those descendants include recurring and one-time logon command registrations and policy containers for the Windows shell and related interfaces. The literal name is a registry namespace convention, not proof of a particular operating-system version, installed release, or configuration state. Its children determine the actual feature involved.

## Atomic claim

Provides the version-named parent for documented user logon and Windows policy locations.

Scope: **user**

## Meaning in system-level logs

Use the full suffix to distinguish Run, RunOnce, and Policies in registry telemetry. The prefix name cannot establish an OS build; collect host version metadata separately.

### What the path cannot establish

- The parent prefix does not specify a child policy value or establish its enabled state.
- An access to this namespace does not prove the descendant feature was used or that a requested change succeeded.

### Applicability

Structural namespace inferred from the cited documented descendants. Each descendant has its own Windows version, feature, and policy-scope requirements.


### Claim-level evidence

- **structural_inference** — Both documented per-user logon locations are beneath this prefix.
  Section: Run and RunOnce Registry Keys.
  - [https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys>)
- **structural_inference** — The user Comdlg32 policy establishes the common-dialog policy ancestry under this namespace.
  Section: NoBackButton / ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nobackbutton](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nobackbutton>)
- **structural_inference** — The user System policy establishes the system-policy descendant under this namespace.
  Section: CustomShell / ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#customshell](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#customshell>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nobackbutton](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nobackbutton>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#customshell](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#customshell>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunoncelegacy&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunoncelegacy_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#nowelcometips&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#nowelcometips_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#run&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#run_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nodeleteprinter](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nodeleteprinter>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disableregedit](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disableregedit>)
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
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#limitsize](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#limitsize>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#classicshell](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#classicshell>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#confirmfiledelete](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#confirmfiledelete>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablebinddirectlytopropertysetstorage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablebinddirectlytopropertysetstorage>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enforceshellextensionsecurity](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enforceshellextensionsecurity>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#linkresolveignorelinkinfo](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#linkresolveignorelinkinfo>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#maxrecentdocs](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#maxrecentdocs>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nobackbutton](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nobackbutton>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nocachethumbnailpictures](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nocachethumbnailpictures>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nocdburning](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nocdburning>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nochangeanimation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nochangeanimation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nochangekeyboardnavigationindicators](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nochangekeyboardnavigationindicators>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nodfstab](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nodfstab>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nodrives](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nodrives>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noentirenetwork](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noentirenetwork>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofilemenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofilemenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofilemru](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofilemru>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofolderoptions](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofolderoptions>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nohardwaretab](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nohardwaretab>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nomanagemycomputerverb](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nomanagemycomputerverb>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nomycomputershareddocuments](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nomycomputershareddocuments>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nonetconnectdisconnect](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nonetconnectdisconnect>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noplacesbar](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noplacesbar>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#norecyclefiles](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#norecyclefiles>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#norunasinstallprompt](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#norunasinstallprompt>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nosecuritytab](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nosecuritytab>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noshellsearchbutton](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noshellsearchbutton>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nostrcmplogical](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nostrcmplogical>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noviewcontextmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noviewcontextmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noviewondrive](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noviewondrive>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nowindowshotkeys](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nowindowshotkeys>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noworkgroupcontents](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noworkgroupcontents>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#placesbar](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#placesbar>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#promptrunasinstallnetpath](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#promptrunasinstallnetpath>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#recyclebinsize](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#recyclebinsize>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#shellprotocolprotectedmodetitle&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#shellprotocolprotectedmodetitle_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#customshell](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#customshell>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#logonhoursnotificationpolicydescription](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#logonhoursnotificationpolicydescription>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#logonhourspolicydescription](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#logonhourspolicydescription>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#reportcachedlogonpolicydescription](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#reportcachedlogonpolicydescription>)
- [https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
