---
node_id: "knowledge:bcca618a2ebe720c2fa40e72"
generated: true
---

# v6Transition

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\TCPIP\v6Transition
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:bcca618a2ebe720c2fa40e72`

## Hierarchy

Parent: [TCPIP](knowledge-35950a0f066a3ad7fbbffa69.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: directaccess&#95;routing&#95;policy

This machine TCPIP v6Transition policy key contains the reviewed DirectAccess force-tunneling setting. It determines whether a remote DirectAccess client sends Internet traffic through the internal network or uses its local default gateway directly. The key name reflects the networking policy context, but the documented setting has a specific DirectAccess scope rather than a general promise about all IPv6 transitions or VPN routing.

## Atomic claim

Stores DirectAccess policy for routing remote-client Internet traffic through the internal network.

Scope: **machine**

## Meaning in system-level logs

An access here concerns DirectAccess routing policy. Inspect the particular configured option, data, operation, and result; actual tunnel establishment or routed traffic requires DirectAccess state, route information, and network evidence.

### What the path cannot establish

- The key does not prove DirectAccess is deployed or a tunnel is active.
- It does not establish the route used by a particular packet or apply automatically to every VPN.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. The behavior requires a supported DirectAccess client/deployment; CSP mapping availability is not evidence that DirectAccess is present on every listed edition or release.


### Claim-level evidence

- **direct** — The force-tunneling policy maps here and controls Internet routing for remote DirectAccess clients.
  Section: NC&#95;ForceTunneling.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;forcetunneling](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_forcetunneling>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;forcetunneling](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_forcetunneling>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;forcetunneling](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_forcetunneling>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
