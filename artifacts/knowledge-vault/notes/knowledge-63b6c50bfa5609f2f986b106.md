---
node_id: "knowledge:63b6c50bfa5609f2f986b106"
generated: true
---

# Notifyees

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Control\NetworkProvider\Notifyees
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:63b6c50bfa5609f2f986b106`

## Hierarchy

Parent: [NetworkProvider](knowledge-c25d1e41d0885923e3abc8f3.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: connection&#95;notification&#95;registrations

Notifyees registers DLLs that receive network connection notifications. Each registration is a named value whose data supplies the notification DLL location. The value names are chosen by the registering application, so they are not a fixed set of child keys. Interpret a record here as notification registration data and obtain runtime evidence before claiming that any callback was invoked for a real connection.

## Atomic claim

Notifyees registers DLLs that receive network connection notifications.

Scope: **machine**

## Meaning in system-level logs

A Notifyees event needs the value name, DLL path data, actor and operation result; connection events are separate evidence.

### What the path cannot establish

- A value registration does not establish callback execution.
- The key does not identify a network destination or connection result.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **Application-named registrations** (value_collection): REG&#95;EXPAND&#95;SZ paths to connection-notification DLLs.

### Claim-level evidence

- **direct** — Notifyees accepts named REG&#95;EXPAND&#95;SZ DLL-path values.
  Section: Connection notification registration.
  - [https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
