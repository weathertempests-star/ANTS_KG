---
node_id: "knowledge:35950a0f066a3ad7fbbffa69"
generated: true
---

# TCPIP

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\TCPIP
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:35950a0f066a3ad7fbbffa69`

## Hierarchy

Parent: [Windows](knowledge-448d4b3e7d83a6ebe3c51a2d.md)

Children:

- [v6Transition](knowledge-bcca618a2ebe720c2fa40e72.md)

## Functional explanation

Status: **structural**

Role: tcpip&#95;policy&#95;namespace

This machine TCPIP policy namespace is the parent of the documented v6Transition branch used by the DirectAccess force-tunneling policy. Its role in this inventory is inferred from that child mapping. It should not be treated as a complete TCP/IP configuration store: adapter addresses, routes, protocol state, and ordinary service parameters are not established by reaching this software policy prefix.

## Atomic claim

Groups the machine TCP/IP policy branch for IPv6 transition and DirectAccess behavior.

Scope: **machine**

## Meaning in system-level logs

Continue to v6Transition and the specific force-tunneling setting when interpreting this target. The registry operation, result, and data describe configuration access; actual traffic routing requires route or network observations.

### What the path cannot establish

- The prefix does not show IPv6 is enabled or a transition tunnel exists.
- It does not identify a route, an IP address, or any connection that used DirectAccess.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.


### Claim-level evidence

- **structural_inference** — DirectAccess Internet traffic routing policy maps to the v6Transition child of this TCPIP prefix.
  Section: NC&#95;ForceTunneling.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;forcetunneling](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_forcetunneling>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;forcetunneling](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_forcetunneling>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;forcetunneling](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_forcetunneling>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
