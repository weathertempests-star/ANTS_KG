---
node_id: "knowledge:20effaab1b56130d0f0a4f4c"
generated: true
---

# PackagePointAndPrint

## Full prefix

~~~text
HKCU\Software\Policies\Microsoft\Windows NT\Printers\PackagePointAndPrint
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:20effaab1b56130d0f0a4f4c`

## Hierarchy

Parent: [Printers](knowledge-199b7b1f8ced6c8b25f2904c.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;package&#95;point&#95;and&#95;print&#95;policies

PackagePointAndPrint is the documented user policy key for restricting printer connections to package-aware drivers and, separately, approved print servers. Package Point and Print checks signatures on downloaded drivers. The approved-server policy applies to package connections and is independent of the policy for non-package Point and Print; Microsoft documents that clients can attempt a non-package connection after package connection failure. This key alone therefore does not establish a complete printer-connection boundary.

## Atomic claim

Stores user restrictions for package-aware Point and Print connections.

Scope: **user**

## Meaning in system-level logs

Inspect the package-only state, approved-server state/list, OS baseline, and other applicable print policies. Correlate print-service or driver-installation records before claiming a connection or driver installation occurred.

### What the path cannot establish

- An approved-server policy here alone does not block every non-package printer connection.
- A policy value does not identify an installed driver or prove a printer connection succeeded.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **PackagePointAndPrintOnly** (value): Policy state restricting Point and Print to package-aware printer drivers.
- **PackagePointAndPrintServerList** (value): Policy state for the approved-server restriction; the server-list contents are additional configuration.

### Claim-level evidence

- **direct** — Microsoft documents package-only behavior, approved servers, and possible non-package fallback at this user policy key.
  Section: PackagePointAndPrintOnly; PackagePointAndPrintServerList / descriptions and ADMX mappings.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
