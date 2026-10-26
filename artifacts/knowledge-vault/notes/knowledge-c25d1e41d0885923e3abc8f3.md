---
node_id: "knowledge:c25d1e41d0885923e3abc8f3"
generated: true
---

# NetworkProvider

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Control\NetworkProvider
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:c25d1e41d0885923e3abc8f3`

## Hierarchy

Parent: [Control](knowledge-cf70125942441319173f4965.md)

Children:

- [Notifyees](knowledge-63b6c50bfa5609f2f986b106.md)
- [Order](knowledge-836a38d0f6b9373d181f66ad.md)

## Functional explanation

Status: **structural**

Role: network&#95;provider&#95;control&#95;namespace

NetworkProvider groups system-level provider ordering and connection-notification registration. The documented Order and Notifyees children establish this shared parent. Provider-specific implementation details are stored separately beneath the corresponding Services entry. Keep the two roles distinct: a registry observation at this parent identifies provider control configuration, but does not by itself select a DLL, authenticate a user or establish a network connection.

## Atomic claim

NetworkProvider groups system-level provider ordering and connection-notification registration.

Scope: **machine**

## Meaning in system-level logs

A provider-control event needs the Order or Notifyees descendant and its value data to identify the changed configuration.

### What the path cannot establish

- The parent does not identify a particular network provider DLL.
- A provider-control reference does not demonstrate a connection or credential event.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **structural_inference** — Order and Notifyees locate shared network-provider control below this parent.
  Section: Provider ordering and connection notifications.
  - [https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
