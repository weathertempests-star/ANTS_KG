---
node_id: "knowledge:6ab6ed011cc1f7551c095b92"
generated: true
---

# 1

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\1
~~~

- Domain: registry
- Depth: L9
- Node ID: `knowledge:6ab6ed011cc1f7551c095b92`

## Hierarchy

Parent: [Zones](knowledge-7156d159a3d7537246fc2770.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: machine&#95;intranet&#95;zone&#95;action&#95;policy

This key holds machine-scoped action policies for the Local Intranet URL security zone, numbered 1. Microsoft maps File Explorer Search Connector query permission to 180E and preview/custom-thumbnail permission to 180F here. Local Intranet is zone ID 1; a policy for it does not identify a physical LAN, adapter, or contacted intranet server. Stored policy data must be distinguished from site assignments and actual application activity.

## Atomic claim

Configures machine Local Intranet action policies, including File Explorer OpenSearch query and preview permissions.

Scope: **machine**

## Meaning in system-level logs

For logs under this machine Local Intranet key, retain the action value, prior/new data, operation result, and consumer identity. Use URL-zone mapping and query/preview records to identify any actual intranet resource access.

### What the path cannot establish

- The path does not identify a URL or prove that any query, preview, thumbnail retrieval, or browser navigation occurred.
- The named action values and their data, applicable policy selection, and consuming component are required to determine effective permissions.

### Applicability

The cited File Explorer ADMX CSP mappings support user and device scopes on Windows 10 with the listed KB5005101 baselines and Windows 11 21H2 or later in the documented managed editions. URL-zone concepts also belong to the legacy Internet Explorer platform; IE11 desktop retirement does not imply removal of all zone consumers. Edge IE mode supports security-zone policies; this is not a general Chromium navigation policy. The documented 180F preview/custom-thumbnail setting may await user logoff before a change applies.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **180E** (value): Policy action governing File Explorer Search Connector OpenSearch queries for this zone; enabled permits and disabled denies. The documented unconfigured state permits queries.
- **180F** (value): Policy action governing previews and custom thumbnails for this zone; enabled permits and disabled denies. The documented unconfigured state permits them; thumbnails are evaluated using their own zone. Changes may take effect only after the user logs off.

### Claim-level evidence

- **direct** — Microsoft maps 180E to this exact Local Intranet zone path in both Computer and User Configuration.
  Section: IZ&#95;Policy&#95;OpenSearchQuery&#95;Intranet / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;intranet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_intranet>)
- **direct** — Microsoft maps 180F here for previews and custom thumbnails; the thumbnail’s own zone is checked.
  Section: IZ&#95;Policy&#95;OpenSearchPreview&#95;Intranet / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;intranet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_intranet>)
- **direct** — The documented zone identifier 1 denotes Local Intranet.
  Section: Zones.
  - [https://learn.microsoft.com/en-us/previous-versions/troubleshoot/browsers/security-privacy/ie-security-zones-registry-entries](<https://learn.microsoft.com/en-us/previous-versions/troubleshoot/browsers/security-privacy/ie-security-zones-registry-entries>)
- **direct** — IE mode supports Internet Explorer security-zone settings and group policies.
  Section: What is IE mode? / supported Internet Explorer functionality.
  - [https://learn.microsoft.com/en-us/deployedge/edge-ie-mode](<https://learn.microsoft.com/en-us/deployedge/edge-ie-mode>)
- **direct** — IE11 desktop support ended for Windows 10 semi-annual channel on June 15, 2022; retirement scope is not every Windows component.
  Section: Internet Explorer 11 / Important.
  - [https://learn.microsoft.com/en-us/lifecycle/products/internet-explorer-11](<https://learn.microsoft.com/en-us/lifecycle/products/internet-explorer-11>)
- **direct** — Preview policy changes may not apply until the user logs off.
  Section: OpenSearch preview policy description.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;intranet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_intranet>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **SCOPE_COUNTERPART_OF** (incoming): [1](knowledge-b70041dd444cd0fea641a258.md)
  These documented action-policy mappings exist in both User Configuration and Computer Configuration; the two hive locations have different scope and neither path alone determines the effective policy.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)
- **LOCKDOWN_COUNTERPART_OF** (incoming): [1](knowledge-a7d949e76387efd3c19bdad9.md)
  The same numeric URL zone has separate ordinary and locked-down policy sets; the documented lockdown features compare those equivalent-zone settings, without the key alone enabling lockdown.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;intranet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_intranet>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;intranet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_intranet>)
- [https://learn.microsoft.com/en-us/previous-versions/troubleshoot/browsers/security-privacy/ie-security-zones-registry-entries](<https://learn.microsoft.com/en-us/previous-versions/troubleshoot/browsers/security-privacy/ie-security-zones-registry-entries>)
- [https://learn.microsoft.com/en-us/deployedge/edge-ie-mode](<https://learn.microsoft.com/en-us/deployedge/edge-ie-mode>)
- [https://learn.microsoft.com/en-us/lifecycle/products/internet-explorer-11](<https://learn.microsoft.com/en-us/lifecycle/products/internet-explorer-11>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;intranet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_intranet>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;intranet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_intranet>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
