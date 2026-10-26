---
node_id: "knowledge:1c488ca7b6bc263a06dc1a5d"
generated: true
---

# Service

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\WinRM\Service
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:1c488ca7b6bc263a06dc1a5d`

## Hierarchy

Parent: [WinRM](knowledge-89f201b64adc5b339389bdd7.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: winrm&#95;service&#95;authentication&#95;policy

This machine WinRM Service policy key stores administrative control over whether the Windows Remote Management service accepts Kerberos credentials over the network. Microsoft maps DisallowKerberos&#95;1 to the AllowKerberos value at this location. The service role handles incoming authentication and differs from the sibling Client policy for outgoing direct Kerberos use. This setting does not itself create a listener or authorize a particular remote task.

## Atomic claim

Controls acceptance of Kerberos credentials by the local WinRM service.

Scope: **machine**

## Meaning in system-level logs

Inspect AllowKerberos data with registry operation and result, accounting for the disallow policy wording. Actual inbound authentication needs service/session records identifying the client, mechanism, result, and any later authorization decision.

### What the path cannot establish

- A policy key does not establish a reachable WinRM listener.
- Kerberos acceptance policy does not prove a user authenticated, was authorized, or ran a remote command.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **AllowKerberos** (value): Controls WinRM service acceptance of Kerberos authentication; the documented policy is phrased as disallowing it.

### Claim-level evidence

- **direct** — The service disallow policy maps to AllowKerberos here and controls acceptance of Kerberos credentials over the network.
  Section: DisallowKerberos&#95;1.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_1>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **COMPLEMENTARY_AUTHENTICATION_ROLE** (incoming): [Client](knowledge-d2343a9ac128221d53510a12.md)
  The WinRM client policy governs outgoing direct Kerberos use, while the service policy governs incoming acceptance of Kerberos credentials; the same value name must be read in its role-specific path.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_2>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_1>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_1>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_1>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
