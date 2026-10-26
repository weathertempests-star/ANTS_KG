---
node_id: "knowledge:3b0ebbbbf03c092bb0f82e6d"
generated: true
---

# Network

## Full prefix

~~~text
HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Network
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:3b0ebbbbf03c092bb0f82e6d`

## Hierarchy

Parent: [Policies](knowledge-0c0778e8b36d2e9810ea000d.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;network&#95;resource&#95;browsing&#95;policy

This Network key is the documented user policy location for NoEntireNetwork, which changes the network-resource lists shown by File Explorer and Network Locations. The setting removes browsing choices for computers outside the user’s workgroup or local domain when enabled. It governs interface discovery, rather than forming a general network-access boundary: Microsoft states that users can still connect to remote computers through other methods, including an explicitly entered share name.

## Atomic claim

Stores the user policy controlling Entire Network browsing in supported shell interfaces.

Scope: **user**

## Meaning in system-level logs

For a log here, inspect NoEntireNetwork data and the relevant shell version. A browsing-policy change cannot be interpreted as a firewall change or evidence that a remote connection was blocked.

### What the path cannot establish

- The policy does not prohibit all remote computer or share access.
- The path does not identify a contacted host, successful network connection, or discovered computer.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **NoEntireNetwork** (value): User policy for removing Entire Network browsing choices and out-of-workgroup/domain computer icons in supported shell lists.

### Claim-level evidence

- **direct** — Microsoft maps NoEntireNetwork here and distinguishes removed browsing choices from other connection methods.
  Section: NoEntireNetwork / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noentirenetwork](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noentirenetwork>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noentirenetwork](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noentirenetwork>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noentirenetwork](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noentirenetwork>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
