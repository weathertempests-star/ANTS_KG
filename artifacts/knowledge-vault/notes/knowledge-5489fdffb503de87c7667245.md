---
node_id: "knowledge:5489fdffb503de87c7667245"
generated: true
---

# System

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\System
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:5489fdffb503de87c7667245`

## Hierarchy

Parent: [Windows](knowledge-448d4b3e7d83a6ebe3c51a2d.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: windows&#95;system&#95;administrative&#95;policy

This machine Windows System policy key hosts several administrative-template families, including sign-in presentation, user-profile handling, credential-provider defaults, SmartScreen, and fast startup. These settings share a registry location rather than one universal System switch. It differs from CurrentVersion Policies System, where other logon and authentication settings reside. The value name is essential for identifying which lifecycle or protection mechanism is being configured.

## Atomic claim

Stores machine policies for sign-in presentation, profiles, credential defaults, SmartScreen, and startup behavior.

Scope: **machine**

## Meaning in system-level logs

Inspect the exact value, data, operation, and result to distinguish UI settings from profile handling or SmartScreen policy. Registry access alone does not demonstrate sign-in, profile deletion, a protection warning, or a fast-startup boot.

### What the path cannot establish

- The key does not establish whether SmartScreen is enabled or a downloaded application was blocked.
- Its presence does not show a user signed in, a profile was unloaded, or a startup operation occurred.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. Profile, Connected Standby, shell, and fast-startup settings have distinct feature prerequisites; the fast-startup policy requires hibernation and does not prove it is operational.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **BlockUserFromShowingAccountDetailsOnSignin** (value): Controls preventing users from choosing to display account details at sign-in.
- **DisableForceUnload** (value): Controls preventing forced user-registry unloading while open handles remain.
- **EnableSmartScreen** (value): Controls SmartScreen enablement for downloaded application checks.
- **HiberbootEnabled** (value): Controls the fast-startup requirement policy.

### Claim-level evidence

- **direct** — The named value controls showing account details on the sign-in screen.
  Section: BlockUserFromShowingAccountDetailsOnSignin.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#blockuserfromshowingaccountdetailsonsignin](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#blockuserfromshowingaccountdetailsonsignin>)
- **direct** — DisableForceUnload controls forced user-registry unloading at sign-out.
  Section: DontForceUnloadHive.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#dontforceunloadhive](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#dontforceunloadhive>)
- **direct** — The default credential-provider selection policy maps here.
  Section: DefaultCredentialProvider.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#defaultcredentialprovider](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#defaultcredentialprovider>)
- **direct** — EnableSmartScreen controls Windows Defender SmartScreen for Internet-downloaded applications.
  Section: EnableSmartScreen.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enablesmartscreen](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enablesmartscreen>)
- **direct** — HiberbootEnabled maps fast-startup policy here and depends on hibernation.
  Section: Hiberboot.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-wininit#hiberboot](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-wininit#hiberboot>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#blockuserfromshowingaccountdetailsonsignin](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#blockuserfromshowingaccountdetailsonsignin>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#dontforceunloadhive](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#dontforceunloadhive>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#defaultcredentialprovider](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#defaultcredentialprovider>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enablesmartscreen](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enablesmartscreen>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-wininit#hiberboot](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-wininit#hiberboot>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#allowdomaindelaylock](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#allowdomaindelaylock>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#defaultcredentialprovider](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#defaultcredentialprovider>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#blockuserfromshowingaccountdetailsonsignin](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#blockuserfromshowingaccountdetailsonsignin>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableacrylicbackgroundonlogon](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableacrylicbackgroundonlogon>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#dontenumerateconnectedusers](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#dontenumerateconnectedusers>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#useoembackground](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#useoembackground>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#cleanupprofiles](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#cleanupprofiles>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#dontforceunloadhive](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#dontforceunloadhive>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#leaveappmgmtdata](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#leaveappmgmtdata>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#profileerroraction](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#profileerroraction>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#slowlinktimeout](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#slowlinktimeout>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#user&#95;home](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#user_home>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#userinfoaccessaction](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#userinfoaccessaction>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enablesmartscreen](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enablesmartscreen>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-wininit#hiberboot](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-wininit#hiberboot>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
