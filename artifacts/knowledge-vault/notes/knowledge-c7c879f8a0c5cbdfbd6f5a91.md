---
node_id: "knowledge:c7c879f8a0c5cbdfbd6f5a91"
generated: true
---

# &lt;UserHive&gt;

## Full prefix

~~~text
HKU\<UserHive>
~~~

- Domain: registry
- Depth: L2
- Node ID: `knowledge:c7c879f8a0c5cbdfbd6f5a91`

## Hierarchy

Parent: [HKU](knowledge-03d1e3aac977743d7870fabf.md)

Children:

- [Environment](knowledge-c03c4329e2273c4634c1e2bb.md)
- [Software](knowledge-9c1888fb225c292950b4d253.md)

## Functional explanation

Status: **documented**

Role: user&#95;hive&#95;identity&#95;template

A UserHive child represents a loaded user-profile registry context. The placeholder is an identity slot, not a literal SID or a guarantee that a particular account is signed in. Environment and software settings below it belong to the resolved hive context. A log interpretation must bind the actual child name using account or hive-loading evidence, while keeping user identity separate from the process that accessed the data.

## Atomic claim

A UserHive child represents a loaded user-profile registry context.

Scope: **user**

## Meaning in system-level logs

Retain the concrete hive identifier, resolved account and accessing process; an accessing process can differ from the profile owner.

### What the path cannot establish

- The placeholder does not prove that an account or loaded hive exists.
- A hive owner is not necessarily the actor who accessed its settings.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — HKEY&#95;USERS contains per-user profile hives.
  Section: User profile hives.
  - [https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-hives](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-hives>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **RESOLVES_USER_CONTEXT_TO** (incoming): [HKCU](knowledge-d68744f168b6667521bae00c.md)
  HKCU maps to a concrete user branch represented by the UserHive schema; the template is not itself a runtime target.
  - [https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys>)

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

- Placeholder component: true
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
