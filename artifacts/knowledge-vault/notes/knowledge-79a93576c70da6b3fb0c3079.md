---
node_id: "knowledge:79a93576c70da6b3fb0c3079"
generated: true
---

# 4

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\4
~~~

- Domain: registry
- Depth: L9
- Node ID: `knowledge:79a93576c70da6b3fb0c3079`

## Hierarchy

Parent: [Zones](knowledge-7156d159a3d7537246fc2770.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: machine&#95;restricted&#95;zone&#95;action&#95;policy

This key holds machine-scoped action policies for the Restricted Sites URL security zone, numbered 4. Microsoft maps File Explorer Search Connector query permission to 180E and preview/custom-thumbnail permission to 180F here. Restricted Sites is zone ID 4; the action settings here are separate from the list of sites assigned to the zone. Stored policy data must be distinguished from site assignments and actual application activity.

## Atomic claim

Configures machine Restricted Sites action policies, including File Explorer OpenSearch query and preview permissions.

Scope: **machine**

## Meaning in system-level logs

For logs under this machine Restricted Sites key, retain the action value, prior/new data, operation result, and consumer identity. The documented unconfigured OpenSearch query and preview defaults deny these actions, unlike zones 0–3; establish actual policy state before interpreting an event.

### What the path cannot establish

- The path does not identify a URL or prove that any query, preview, thumbnail retrieval, or browser navigation occurred.
- The named action values and their data, applicable policy selection, and consuming component are required to determine effective permissions.
- Restricted Sites action policy does not enumerate the domains assigned to this zone.

### Applicability

The cited File Explorer ADMX CSP mappings support user and device scopes on Windows 10 with the listed KB5005101 baselines and Windows 11 21H2 or later in the documented managed editions. URL-zone concepts also belong to the legacy Internet Explorer platform; IE11 desktop retirement does not imply removal of all zone consumers. Edge IE mode supports security-zone policies; this is not a general Chromium navigation policy. The documented 180F preview/custom-thumbnail setting may await user logoff before a change applies.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **180E** (value): Policy action governing File Explorer Search Connector OpenSearch queries for this zone; enabled permits and disabled denies. The documented unconfigured state denies queries.
- **180F** (value): Policy action governing previews and custom thumbnails for this zone; enabled permits and disabled denies. The documented unconfigured state denies them; thumbnails are evaluated using their own zone. Changes may take effect only after the user logs off.

### Claim-level evidence

- **direct** — Microsoft maps 180E to this exact Restricted Sites zone path in both Computer and User Configuration.
  Section: IZ&#95;Policy&#95;OpenSearchQuery&#95;Restricted / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;restricted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_restricted>)
- **direct** — Microsoft maps 180F here for previews and custom thumbnails; the thumbnail’s own zone is checked.
  Section: IZ&#95;Policy&#95;OpenSearchPreview&#95;Restricted / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;restricted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_restricted>)
- **direct** — The documented zone identifier 4 denotes Restricted Sites.
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
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;restricted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_restricted>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **SCOPE_COUNTERPART_OF** (incoming): [4](knowledge-9bd7e4c73c27ed6760f23280.md)
  These documented action-policy mappings exist in both User Configuration and Computer Configuration; the two hive locations have different scope and neither path alone determines the effective policy.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)
- **LOCKDOWN_COUNTERPART_OF** (incoming): [4](knowledge-3f27eaa4cede006bc61684b5.md)
  The same numeric URL zone has separate ordinary and locked-down policy sets; the documented lockdown features compare those equivalent-zone settings, without the key alone enabling lockdown.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-internetexplorer#allowlocalmachinezonetemplate>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;restricted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_restricted>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;restricted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_restricted>)
- [https://learn.microsoft.com/en-us/previous-versions/troubleshoot/browsers/security-privacy/ie-security-zones-registry-entries](<https://learn.microsoft.com/en-us/previous-versions/troubleshoot/browsers/security-privacy/ie-security-zones-registry-entries>)
- [https://learn.microsoft.com/en-us/deployedge/edge-ie-mode](<https://learn.microsoft.com/en-us/deployedge/edge-ie-mode>)
- [https://learn.microsoft.com/en-us/lifecycle/products/internet-explorer-11](<https://learn.microsoft.com/en-us/lifecycle/products/internet-explorer-11>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;restricted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_restricted>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;restricted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_restricted>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
