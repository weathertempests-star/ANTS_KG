---
node_id: "knowledge:294cb40b081d15e04d353cb7"
generated: true
---

# PackagePointAndPrint

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows NT\Printers\PackagePointAndPrint
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:294cb40b081d15e04d353cb7`

## Hierarchy

Parent: [Printers](knowledge-3b4c71166c9c7fba64853b39.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: package&#95;point&#95;and&#95;print&#95;policy

This machine Printers PackagePointAndPrint policy key controls package-aware printer connections and approved servers for those connections. Package-only policy requires package-aware drivers and their signature checks. Approved-server policy applies specifically to package Point and Print, independently of non-package Point and Print restrictions. Microsoft documents non-package fallback on applicable clients, so an approved package-server list alone is not a universal print-server block.

## Atomic claim

Controls package-aware printer connections and approved package print servers.

Scope: **machine**

## Meaning in system-level logs

Inspect the policy enable values and configured server entries with registry operation and result. To establish a connection or driver installation, require the actual print-server target, connection type, driver identity, and outcome.

### What the path cannot establish

- This path does not show a printer connection or driver download occurred.
- The package approved-server policy alone does not prove non-package connections to other servers are blocked.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. The Win7 suffix identifies the documented machine policy variant; the policy description discusses package/non-package fallback for Windows Vista and later, not a guarantee of identical printing security behavior on every release.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **PackagePointAndPrintOnly** (value): Controls restriction to package-aware Point and Print connections.
- **PackagePointAndPrintServerList** (value): Enable control for approved package Point and Print servers; the selected server entries are separate data.

### Claim-level evidence

- **direct** — PackagePointAndPrintOnly restricts clients to package-aware Point and Print and associated driver signature checking.
  Section: PackagePointAndPrintOnly&#95;Win7.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly&#95;win7](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly_win7>)
- **direct** — PackagePointAndPrintServerList governs approved package servers independently of non-package restrictions; the description warns about fallback.
  Section: PackagePointAndPrintServerList&#95;Win7.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist&#95;win7](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist_win7>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly&#95;win7](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly_win7>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist&#95;win7](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist_win7>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly&#95;win7](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly_win7>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist&#95;win7](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist_win7>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
