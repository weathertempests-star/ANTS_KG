---
node_id: "knowledge:4c4a0a5b8a3c06a3572606b7"
generated: true
---

# Windows

## Full prefix

~~~text
HKLM\Software\Microsoft\Windows
~~~

- Domain: registry
- Depth: L4
- Node ID: `knowledge:4c4a0a5b8a3c06a3572606b7`

## Hierarchy

Parent: [Microsoft](knowledge-acd43835e6c7c037c564c959.md)

Children:

- [CurrentVersion](knowledge-6202b8718fe33a7616eb9084.md)

## Functional explanation

Status: **structural**

Role: windows&#95;configuration&#95;namespace

Windows groups machine software configuration belonging to the Windows product namespace. The documented Run and Uninstall paths pass through its CurrentVersion child. This product-level grouping is distinct from the adjacent Windows NT namespace and from the SYSTEM hive used for active control-set configuration. Resolve the next child before assigning startup-registration, product-inventory or other feature meaning to an observation.

## Atomic claim

Windows groups machine software configuration belonging to the Windows product namespace.

Scope: **machine**

## Meaning in system-level logs

A log targeting this prefix identifies the Windows product namespace under machine software. Preserve the next child and operation to determine which facility was accessed.

### What the path cannot establish

- The product namespace does not identify the installed Windows release.
- It does not establish a change to SYSTEM control-set configuration.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **structural_inference** — The documented uninstall location establishes this Windows configuration ancestor.
  Section: Uninstall registry path.
  - [https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key](<https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key>)
- **structural_inference** — The documented machine startup-registration paths pass through this namespace.
  Section: Four Run and RunOnce registry locations.
  - [https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key](<https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key>)
- [https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys>)

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
- [https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key](<https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key>)
- [https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
