---
node_id: "knowledge:da597a2f1a374e635b122f88"
generated: true
---

# System

## Full prefix

~~~text
HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:da597a2f1a374e635b122f88`

## Hierarchy

Parent: [Policies](knowledge-623ca3b4b145b4d7cffd200e.md)

Children:

- [Audit](knowledge-cfe58fa3f58d656bd954fcc9.md)
- [Kerberos](knowledge-f90cfc165ebfddf19229f879.md)

## Functional explanation

Status: **documented**

Role: system&#95;policy&#95;configuration

This machine System policy key stores administrative settings used during startup, sign-in, sign-out, and shutdown, with dedicated descendants for auditing and Kerberos. Direct settings include status-message display, credential-provider exclusion, previous-logon information, software-generated secure attention sequences, and legacy shutdown behavior. It describes configuration for these mechanisms; it is not a history of authentication attempts or system shutdowns.

## Atomic claim

Stores machine controls for sign-in presentation, credential-provider selection, and system session behavior.

Scope: **machine**

## Meaning in system-level logs

A target at this key needs the specific value, operation, result, and data to distinguish a status-display setting from credential-provider or sign-in policy. Actual authentication results require separate authentication telemetry.

### What the path cannot establish

- Its presence does not establish authentication success or failure.
- The path does not identify an excluded credential provider or show the exclusion is effective.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **DisableStatusMessages** (value): Controls suppression of startup, shutdown, logon, and logoff status messages.
- **DisplayLastLogonInfo** (value): Controls display of previous sign-in and failure information.

### Claim-level evidence

- **direct** — DisableStatusMessages maps system status-message suppression to this key.
  Section: DisableStatusMessages.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disablestatusmessages](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disablestatusmessages>)
- **direct** — The exclusion policy specifies credential-provider CLSIDs at this key.
  Section: ExcludedCredentialProviders.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#excludedcredentialproviders](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#excludedcredentialproviders>)
- **direct** — DisplayLastLogonInfo controls display of previous logons and failures.
  Section: DisplayLastLogonInfoDescription.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#displaylastlogoninfodescription](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#displaylastlogoninfodescription>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disablestatusmessages](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disablestatusmessages>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#excludedcredentialproviders](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#excludedcredentialproviders>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#displaylastlogoninfodescription](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#displaylastlogoninfodescription>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#excludedcredentialproviders](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#excludedcredentialproviders>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#alwayssendcompoundid](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#alwayssendcompoundid>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#devicepkinitenabled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#devicepkinitenabled>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#hosttorealm](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#hosttorealm>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxydisableserverrevocationcheck](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxydisableserverrevocationcheck>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxyserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxyserver>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#mitrealms](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#mitrealms>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#stricttarget](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#stricttarget>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disablestatusmessages](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disablestatusmessages>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#verbosestatus](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#verbosestatus>)
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
