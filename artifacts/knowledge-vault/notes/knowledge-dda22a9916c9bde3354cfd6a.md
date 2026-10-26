---
node_id: "knowledge:dda22a9916c9bde3354cfd6a"
generated: true
---

# Winlogon

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows NT\CurrentVersion\Winlogon
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:dda22a9916c9bde3354cfd6a`

## Hierarchy

Parent: [CurrentVersion](knowledge-be5a4d3eb6874a0e96ffbe30.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: foreground&#95;group&#95;policy&#95;configuration

This machine Windows NT CurrentVersion Winlogon policy key stores SyncForegroundPolicy, which controls waiting for network initialization and applying Group Policy synchronously during startup and sign-in. It concerns processing order rather than credentials or automatic logon. Microsoft documents special Windows Server behavior, where startup processing can already be synchronous and sign-in handling depends on the server configuration described in the policy.

## Atomic claim

Controls waiting for network initialization and foreground Group Policy processing at startup and logon.

Scope: **machine**

## Meaning in system-level logs

Inspect SyncForegroundPolicy data with registry operation and result. To establish that a startup or sign-in actually waited for the network or completed policy processing, correlate with Group Policy operational records and the machine role.

### What the path cannot establish

- The key does not establish a user signed in or a policy cycle succeeded.
- The setting alone cannot determine timing on every Windows Server role or configuration.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. Windows Server 2008 and later ignore this setting for startup processing, which is synchronous; its effect at server logon depends on the documented Terminal Services/asynchronous-processing configuration.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **SyncForegroundPolicy** (value): Controls network waiting and synchronous foreground Group Policy processing where the policy applies.

### Claim-level evidence

- **direct** — SyncForegroundPolicy maps here and controls waiting for network initialization and synchronous foreground Group Policy, with Windows Server exceptions.
  Section: SyncForegroundPolicy.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
