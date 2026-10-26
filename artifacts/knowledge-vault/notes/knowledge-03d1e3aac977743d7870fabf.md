---
node_id: "knowledge:03d1e3aac977743d7870fabf"
generated: true
---

# HKU

## Full prefix

~~~text
HKU
~~~

- Domain: registry
- Depth: L1
- Node ID: `knowledge:03d1e3aac977743d7870fabf`

## Hierarchy

Parent: Root

Children:

- [.DEFAULT](knowledge-c964826ca6b8eaef9932d78d.md)
- [&lt;UserHive&gt;](knowledge-c7c879f8a0c5cbdfbd6f5a91.md)

## Functional explanation

Status: **documented**

Role: loaded&#95;user&#95;hives&#95;root

HKU contains loaded user-profile registry branches. Each profile branch supplies a context for preferences and other per-user configuration. The root is broader than the current interactive user and should not be treated as a list of people actively using the computer. A log record needs its concrete child identity and process context to distinguish an ordinary user profile from a system-account profile or another mounted hive.

## Atomic claim

HKU contains loaded user-profile registry branches.

Scope: **mixed**

## Meaning in system-level logs

An HKU event needs the concrete hive child, user/SID resolution and full descendant; preserve any evidence of offline or explicit hive mounting.

### What the path cannot establish

- A loaded hive does not prove an interactive sign-in is currently active.
- HKU is not interchangeable with one fixed HKCU user context.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — User-profile hives are located beneath HKEY&#95;USERS.
  Section: User profile hives.
  - [https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-hives](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-hives>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-hives](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-hives>)
- [https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment](<https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment>)
- [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)
- [https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
