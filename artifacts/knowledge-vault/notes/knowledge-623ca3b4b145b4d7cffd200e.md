---
node_id: "knowledge:623ca3b4b145b4d7cffd200e"
generated: true
---

# Policies

## Full prefix

~~~text
HKLM\Software\Microsoft\Windows\CurrentVersion\Policies
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:623ca3b4b145b4d7cffd200e`

## Hierarchy

Parent: [CurrentVersion](knowledge-6202b8718fe33a7616eb9084.md)

Children:

- [Explorer](knowledge-f07cdc68b92830b299c967c3.md)
- [System](knowledge-da597a2f1a374e635b122f88.md)

## Functional explanation

Status: **structural**

Role: policy&#95;namespace

This machine policy namespace groups Windows shell and system administrative settings under the CurrentVersion branch. Its Explorer and System descendants separate desktop restrictions from sign-in, authentication, and auditing controls. The namespace role is inferred from documented descendant mappings rather than a single policy attached to this parent. Meaningful interpretation therefore requires continuing to the named child key and setting.

## Atomic claim

Collects machine policy branches for Windows shell, sign-in, auditing, and authentication.

Scope: **machine**

## Meaning in system-level logs

A registry target ending here identifies a policy namespace. Use the complete descendant path, registry operation, result, and value name/data to identify which administrative setting was queried or changed.

### What the path cannot establish

- The parent path does not identify a particular policy or its configured state.
- An access to this namespace does not establish sign-in, process creation, or policy application.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.


### Claim-level evidence

- **structural_inference** — The Explorer policy mapping is beneath this prefix.
  Section: DisableExplorerRunLegacy&#95;2.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy_2>)
- **structural_inference** — The process-creation command-line policy maps to the System&#92;Audit descendant.
  Section: IncludeCmdLine.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#excludedcredentialproviders](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#excludedcredentialproviders>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#alwayssendcompoundid](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#alwayssendcompoundid>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#devicepkinitenabled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#devicepkinitenabled>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#hosttorealm](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#hosttorealm>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxydisableserverrevocationcheck](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxydisableserverrevocationcheck>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxyserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxyserver>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#mitrealms](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#mitrealms>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#stricttarget](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#stricttarget>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunlegacy_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunoncelegacy&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableexplorerrunoncelegacy_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disablestatusmessages](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disablestatusmessages>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#nowelcometips&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#nowelcometips_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#run&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#run_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#verbosestatus](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#verbosestatus>)
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
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-wininit#disablenamedpipeshutdownpolicydescription](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-wininit#disablenamedpipeshutdownpolicydescription>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-wininit#shutdowntimeouthungsessionsdescription](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-wininit#shutdowntimeouthungsessionsdescription>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#displaylastlogoninfodescription](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#displaylastlogoninfodescription>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#reportcachedlogonpolicydescription](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#reportcachedlogonpolicydescription>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#softwaresasgeneration](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#softwaresasgeneration>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
