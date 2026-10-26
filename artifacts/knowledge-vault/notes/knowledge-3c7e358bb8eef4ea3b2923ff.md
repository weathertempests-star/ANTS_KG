---
node_id: "knowledge:3c7e358bb8eef4ea3b2923ff"
generated: true
---

# 3

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\CurrentVersion\Internet Settings\Lockdown_Zones\3
~~~

- Domain: registry
- Depth: L9
- Node ID: `knowledge:3c7e358bb8eef4ea3b2923ff`

## Hierarchy

Parent: [Lockdown&#95;Zones](knowledge-0038fc7f2000e3953c236541.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: machine&#95;locked&#95;down&#95;internet&#95;zone&#95;action&#95;policy

This key holds machine-scoped action policies for the locked-down Internet URL security zone, numbered 3. Microsoft maps File Explorer Search Connector query permission to 180E and preview/custom-thumbnail permission to 180F here. It is the locked-down counterpart of the same numbered ordinary zone, consulted according to the relevant feature’s lockdown behavior. Stored policy data must be distinguished from site assignments and actual application activity.

## Atomic claim

Configures machine locked-down Internet action policies, including File Explorer OpenSearch query and preview permissions.

Scope: **machine**

## Meaning in system-level logs

For logs under this machine locked-down Internet key, retain the action value, prior/new data, operation result, and consumer identity. Correlate the URL’s zone and the relevant lockdown feature state before treating the locked-down policy as active.

### What the path cannot establish

- The path does not identify a URL or prove that any query, preview, thumbnail retrieval, or browser navigation occurred.
- The named action values and their data, applicable policy selection, and consuming component are required to determine effective permissions.
- A Lockdown&#95;Zones key does not by itself prove lockdown is enabled or that its settings were consulted.

### Applicability

The cited File Explorer ADMX CSP mappings support user and device scopes on Windows 10 with the listed KB5005101 baselines and Windows 11 21H2 or later in the documented managed editions. URL-zone concepts also belong to the legacy Internet Explorer platform; IE11 desktop retirement does not imply removal of all zone consumers. Edge IE mode supports security-zone policies; this is not a general Chromium navigation policy. The documented 180F preview/custom-thumbnail setting may await user logoff before a change applies.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **180E** (value): Policy action governing File Explorer Search Connector OpenSearch queries for this zone; enabled permits and disabled denies. The documented unconfigured state permits queries.
- **180F** (value): Policy action governing previews and custom thumbnails for this zone; enabled permits and disabled denies. The documented unconfigured state permits them; thumbnails are evaluated using their own zone. Changes may take effect only after the user logs off.

### Claim-level evidence

- **direct** — Microsoft maps 180E to this exact locked-down Internet zone path in both Computer and User Configuration.
  Section: IZ&#95;Policy&#95;OpenSearchQuery&#95;InternetLockdown / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;internetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_internetlockdown>)
- **direct** — Microsoft maps 180F here for previews and custom thumbnails; the thumbnail’s own zone is checked.
  Section: IZ&#95;Policy&#95;OpenSearchPreview&#95;InternetLockdown / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;internetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_internetlockdown>)
- **direct** — The documented zone identifier 3 denotes Internet.
  Section: Zones.
  - [https://learn.microsoft.com/en-us/previous-versions/troubleshoot/browsers/security-privacy/ie-security-zones-registry-entries](<https://learn.microsoft.com/en-us/previous-versions/troubleshoot/browsers/security-privacy/ie-security-zones-registry-entries>)
- **direct** — Lockdown features compare an ordinary zone’s settings with its locked-down equivalent.
  Section: AllowLocalMachineZoneTemplate / lockdown note.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate>)
- **direct** — IE mode supports Internet Explorer security-zone settings and group policies.
  Section: What is IE mode? / supported Internet Explorer functionality.
  - [https://learn.microsoft.com/en-us/deployedge/edge-ie-mode](<https://learn.microsoft.com/en-us/deployedge/edge-ie-mode>)
- **direct** — IE11 desktop support ended for Windows 10 semi-annual channel on June 15, 2022; retirement scope is not every Windows component.
  Section: Internet Explorer 11 / Important.
  - [https://learn.microsoft.com/en-us/lifecycle/products/internet-explorer-11](<https://learn.microsoft.com/en-us/lifecycle/products/internet-explorer-11>)
- **direct** — Preview policy changes may not apply until the user logs off.
  Section: OpenSearch preview policy description.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;internetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_internetlockdown>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **SCOPE_COUNTERPART_OF** (incoming): [3](knowledge-6ebdc1863f0a31c5d9929a09.md)
  These documented action-policy mappings exist in both User Configuration and Computer Configuration; the two hive locations have different scope and neither path alone determines the effective policy.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)
- **LOCKDOWN_COUNTERPART_OF** (outgoing): [3](knowledge-7a28dc8f16b6f040a16bc923.md)
  The same numeric URL zone has separate ordinary and locked-down policy sets; the documented lockdown features compare those equivalent-zone settings, without the key alone enabling lockdown.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;internetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_internetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;internetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_internetlockdown>)
- [https://learn.microsoft.com/en-us/previous-versions/troubleshoot/browsers/security-privacy/ie-security-zones-registry-entries](<https://learn.microsoft.com/en-us/previous-versions/troubleshoot/browsers/security-privacy/ie-security-zones-registry-entries>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate>)
- [https://learn.microsoft.com/en-us/deployedge/edge-ie-mode](<https://learn.microsoft.com/en-us/deployedge/edge-ie-mode>)
- [https://learn.microsoft.com/en-us/lifecycle/products/internet-explorer-11](<https://learn.microsoft.com/en-us/lifecycle/products/internet-explorer-11>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;internetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_internetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;internetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_internetlockdown>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
