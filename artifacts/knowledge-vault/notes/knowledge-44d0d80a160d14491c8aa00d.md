---
node_id: "knowledge:44d0d80a160d14491c8aa00d"
generated: true
---

# CurrentVersion

## Full prefix

~~~text
HKCU\Software\Policies\Microsoft\Windows\CurrentVersion
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:44d0d80a160d14491c8aa00d`

## Hierarchy

Parent: [Windows](knowledge-43021d03261165f313b86e60.md)

Children:

- [Internet Settings](knowledge-984950f3b4e37d8f17b93991.md)

## Functional explanation

Status: **structural**

Role: user&#95;windows&#95;version&#95;policy&#95;namespace

This CurrentVersion key is the intermediate parent of documented Windows security-zone policy locations in the user policy tree. The Internet Settings descendants contain separate ordinary and locked-down security-zone branches, including policies used by File Explorer Search Connectors. CurrentVersion is a namespace label rather than an operating-system version report or an active control. Its descendant path and setting data determine the relevant component behavior.

## Atomic claim

Provides the version-named parent of user Internet security-zone policy locations.

Scope: **user**

## Meaning in system-level logs

A log at this prefix identifies user policy namespace context only. Obtain the Internet Settings child path, named value, and data; determine host OS version from host metadata.

### What the path cannot establish

- The CurrentVersion name does not identify the Windows build.
- The ancestor prefix does not determine a zone ID, policy action, or effective setting.

### Applicability

This namespace is established by documented Windows security-zone policies. Underlying feature support and policy precedence must be checked on the specific Windows baseline.


### Claim-level evidence

- **structural_inference** — Computer and User Configuration mappings establish the HKCU ancestor above ordinary and locked-down zone policy keys.
  Section: IZ&#95;Policy&#95;OpenSearchQuery&#95;Internet; IZ&#95;Policy&#95;OpenSearchQuery&#95;InternetLockdown / ADMX mappings.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;internet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_internet>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;internetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_internetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;intranet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_intranet>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;intranetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_intranetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;localmachine](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_localmachine>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;localmachinelockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_localmachinelockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;restricted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_restricted>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;restrictedlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_restrictedlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;trusted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_trusted>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;trustedlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_trustedlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;internet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_internet>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;internetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_internetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;intranet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_intranet>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;intranetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_intranetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;localmachine](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_localmachine>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;localmachinelockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_localmachinelockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;restricted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_restricted>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;restrictedlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_restrictedlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;trusted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_trusted>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;trustedlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_trustedlockdown>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
