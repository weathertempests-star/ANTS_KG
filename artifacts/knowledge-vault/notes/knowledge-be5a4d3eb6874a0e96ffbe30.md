---
node_id: "knowledge:be5a4d3eb6874a0e96ffbe30"
generated: true
---

# CurrentVersion

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows NT\CurrentVersion
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:be5a4d3eb6874a0e96ffbe30`

## Hierarchy

Parent: [Windows NT](knowledge-279dead16457daba15a15074.md)

Children:

- [Winlogon](knowledge-dda22a9916c9bde3354cfd6a.md)

## Functional explanation

Status: **structural**

Role: foreground&#95;policy&#95;processing&#95;namespace

This machine Windows NT CurrentVersion policy namespace is the parent of the documented Winlogon branch for foreground Group Policy synchronization. Its meaning in this inventory is inferred from that descendant mapping. CurrentVersion here organizes the administrative policy path; it is not a registry value containing the installed operating-system version, nor a copy of the ordinary Windows NT CurrentVersion configuration tree.

## Atomic claim

Groups the machine Winlogon policy for synchronous foreground Group Policy processing.

Scope: **machine**

## Meaning in system-level logs

A target ending here identifies only the policy parent. Continue to Winlogon and SyncForegroundPolicy, then use operation, result, and data to interpret the synchronization policy interaction.

### What the path cannot establish

- The parent does not expose an operating-system version or build number.
- It does not show the network was ready or a foreground policy cycle completed.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.


### Claim-level evidence

- **structural_inference** — The foreground processing policy maps to this namespace through the Winlogon child.
  Section: SyncForegroundPolicy.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
