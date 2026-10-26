---
node_id: "knowledge:f07cdc68b92830b299c967c3"
generated: true
---

# Explorer

## Full prefix

~~~text
HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:f07cdc68b92830b299c967c3`

## Hierarchy

Parent: [Policies](knowledge-623ca3b4b145b4d7cffd200e.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: shell&#95;policy&#95;configuration

This machine Explorer policy key holds administrative controls for shell menus, taskbar behavior, and legacy logon run-list processing. It is shared by settings from several administrative templates, so Explorer here identifies the Windows shell policy area rather than a record of browsing folders. Individual value names distinguish UI restrictions, logon-program handling, and other compatibility behavior.

## Atomic claim

Stores machine administrative settings for the shell, Start menu, and legacy logon program handling.

Scope: **machine**

## Meaning in system-level logs

For a target here, inspect the value name and data alongside operation and result. A successful write to HidePowerOptions has a different meaning from reading DisableLocalMachineRun, and neither proves a menu was used or a program started.

### What the path cannot establish

- The key alone does not establish which shell restriction is configured.
- A policy value does not show that a logon program executed or that a shutdown occurred.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. Some descriptions explicitly refer to legacy Windows 2000/XP/Vista shell behavior; applicability must follow the individual setting and current shell.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **DisableLocalMachineRun** (value): Controls whether Windows ignores the legacy machine run list.
- **HidePowerOptions** (value): Controls removal of shutdown, restart, sleep, and hibernate commands from specified UI locations.

### Claim-level evidence

- **direct** — DisableLocalMachineRun controls processing of the legacy machine run list at this key.
  Section: DisableExplorerRunLegacy&#95;2.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy_2>)
- **direct** — HidePowerOptions removes specified power commands from Windows shell and sign-in surfaces; it does not block all programs capable of shutdown.
  Section: HidePowerOptions.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#hidepoweroptions](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#hidepoweroptions>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **HAS_USER_POLICY_COUNTERPART** (outgoing): [Explorer](knowledge-754e0d5a736538dbdaa615d0.md)
  The legacy run-list policy has both machine and user forms; Microsoft states machine configuration takes precedence when both are configured. This precedence statement is specific to the documented setting, not every Explorer policy.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy_2>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#hidepoweroptions](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#hidepoweroptions>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunoncelegacy&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunoncelegacy_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#nowelcometips&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#nowelcometips_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#run&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#run_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#hidepoweroptions](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#hidepoweroptions>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nochangestartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nochangestartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nomoreprogramslist](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nomoreprogramslist>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#norun](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#norun>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosettaskbar](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosettaskbar>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#notraycontextmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#notraycontextmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;nodisconnectmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_nodisconnectmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;nosecuritymenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_nosecuritymenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablebinddirectlytopropertysetstorage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablebinddirectlytopropertysetstorage>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nostrcmplogical](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nostrcmplogical>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#shellprotocolprotectedmodetitle&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#shellprotocolprotectedmodetitle_2>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
