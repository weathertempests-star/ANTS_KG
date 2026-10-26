---
node_id: "knowledge:7a23ffc0cf3da054741fc9ab"
generated: true
---

# Tcpip6

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Services\Tcpip6
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:7a23ffc0cf3da054741fc9ab`

## Hierarchy

Parent: [Services](knowledge-1b4dc8589a4514f201b7f19e.md)

Children:

- [Parameters](knowledge-464f0f015878f5d492bac099.md)

## Functional explanation

Status: **structural**

Role: ipv6&#95;service&#95;configuration

Tcpip6 is the service-tree namespace containing IPv6 configuration. Its documented Parameters child holds DisabledComponents, which controls selected IPv6 behavior. That descendant establishes the scope of this parent without making the parent itself an enable/disable switch. A registry event at Tcpip6 must be resolved to the exact setting before describing address preference, interface configuration or any protocol availability change.

## Atomic claim

Tcpip6 is the service-tree namespace containing IPv6 configuration.

Scope: **machine**

## Meaning in system-level logs

A Tcpip6 event needs the descendant value and restart context to identify an IPv6 configuration change.

### What the path cannot establish

- The parent does not imply IPv6 is disabled.
- The namespace does not show whether a particular IPv6 connection succeeded.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **structural_inference** — The documented IPv6 Parameters path establishes the Tcpip6 ancestor.
  Section: Use registry key to configure IPv6.
  - [https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows](<https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows>)

### Explanation sources

- [https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows](<https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows](<https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
