---
node_id: "knowledge:056ac36fed8c6e9cce9c1170"
generated: true
---

# Lockdown&#95;Zones

## Full prefix

~~~text
HKCU\Software\Policies\Microsoft\Windows\CurrentVersion\Internet Settings\Lockdown_Zones
~~~

- Domain: registry
- Depth: L8
- Node ID: `knowledge:056ac36fed8c6e9cce9c1170`

## Hierarchy

Parent: [Internet Settings](knowledge-984950f3b4e37d8f17b93991.md)

Children:

- [0](knowledge-46fe8c892f18f98435077432.md)
- [1](knowledge-0b0222c9edebfe348697d5f6.md)
- [2](knowledge-85a879912f85e21e02548b39.md)
- [3](knowledge-6ebdc1863f0a31c5d9929a09.md)
- [4](knowledge-bde751d6f32eef5ae8a13495.md)

## Functional explanation

Status: **structural**

Role: user&#95;locked&#95;down&#95;zone&#95;policy&#95;namespace

Lockdown&#95;Zones groups the numbered locked-down security-zone policy keys for the represented user. It parallels Zones without making the two branches interchangeable. Microsoft explains that Local Machine Zone Lockdown and Network Protocol Lockdown compare an active URL’s ordinary-zone settings with the locked-down equivalent. Documented children also hold OpenSearch action policies. The parent is a structural namespace and neither enables lockdown by itself nor guarantees that stored action policies are more restrictive.

## Atomic claim

Groups user policy settings for the locked-down counterparts of URL security zones.

Scope: **user**

## Meaning in system-level logs

Preserve Lockdown&#95;Zones in the logged path and collect the numeric child and action value. Identify the consuming feature and its lockdown context before treating these settings as the ones used for a particular URL.

### What the path cannot establish

- Parent-key presence does not enable a lockdown feature or show it was applied.
- The name does not guarantee stricter values than the ordinary Zones counterpart.

### Applicability

This namespace is established by documented Windows security-zone policies. Underlying feature support and policy precedence must be checked on the specific Windows baseline.


### Claim-level evidence

- **structural_inference** — The documented locked-down Internet action policy establishes this parent.
  Section: IZ&#95;Policy&#95;OpenSearchQuery&#95;InternetLockdown / ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)
- **direct** — Local Machine Zone Lockdown and Network Protocol Lockdown compare ordinary and locked-down equivalent-zone settings.
  Section: AllowLocalMachineZoneTemplate / lockdown note.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;internetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_internetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;intranetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_intranetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;localmachinelockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_localmachinelockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;restrictedlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_restrictedlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;trustedlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_trustedlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;internetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_internetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;intranetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_intranetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;localmachinelockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_localmachinelockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;restrictedlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_restrictedlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;trustedlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_trustedlockdown>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
