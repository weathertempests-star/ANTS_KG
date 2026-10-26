---
node_id: "knowledge:acd43835e6c7c037c564c959"
generated: true
---

# Microsoft

## Full prefix

~~~text
HKLM\Software\Microsoft
~~~

- Domain: registry
- Depth: L3
- Node ID: `knowledge:acd43835e6c7c037c564c959`

## Hierarchy

Parent: [Software](knowledge-a84a70f48e5b3f471e5c2cc0.md)

Children:

- [Cryptography](knowledge-bb7957f37cc434cc4796df7d.md)
- [SystemCertificates](knowledge-1b96f1d311e346ba1fb4b0c9.md)
- [Windows](knowledge-4c4a0a5b8a3c06a3572606b7.md)

## Functional explanation

Status: **structural**

Role: machine&#95;microsoft&#95;namespace

Microsoft is a vendor namespace within machine software configuration. The documented machine certificate-store path passes through this branch, demonstrating one descendant family rather than defining every setting beneath the parent. Keep the next product or subsystem component when interpreting a record. This structural node provides navigation and scope; it does not identify one Microsoft service, policy, certificate or executable.

## Atomic claim

Microsoft is a vendor namespace within machine software configuration.

Scope: **machine**

## Meaning in system-level logs

A record here locates a Microsoft product or subsystem; retain the full descendant, operation and value data before identifying the affected setting.

### What the path cannot establish

- The ancestor alone does not identify a certificate or certificate store.
- The namespace does not establish that any service is running.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **structural_inference** — The documented certificate-store path establishes this ancestor.
  Section: CERT&#95;SYSTEM&#95;STORE&#95;LOCAL&#95;MACHINE.
  - [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

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
- [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)
- [https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
