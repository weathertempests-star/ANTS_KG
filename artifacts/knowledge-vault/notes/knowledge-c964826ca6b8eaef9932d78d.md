---
node_id: "knowledge:c964826ca6b8eaef9932d78d"
generated: true
---

# .DEFAULT

## Full prefix

~~~text
HKU\.DEFAULT
~~~

- Domain: registry
- Depth: L2
- Node ID: `knowledge:c964826ca6b8eaef9932d78d`

## Hierarchy

Parent: [HKU](knowledge-03d1e3aac977743d7870fabf.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: localsystem&#95;profile&#95;configuration

HKU&#92;.DEFAULT is the LocalSystem profile branch, not the template for newly created users. Microsoft identifies it with the LocalSystem account and its S-1-5-18 profile alias. The misleading name must not be used to infer that edits propagate to every future user. For event interpretation, associate the path with system-account profile settings and inspect the actual descendant before identifying a logon-interface or service preference.

## Atomic claim

HKU&#92;.DEFAULT is the LocalSystem profile branch, not the template for newly created users.

Scope: **user**

## Meaning in system-level logs

A .DEFAULT event needs the precise setting and process identity; it may concern system-account profile use rather than a human user preference.

### What the path cannot establish

- A write here does not establish a change to the new-user Default profile template.
- The path alone does not establish that the logon UI used the changed setting.

### Applicability

The Microsoft developer explanation is historical; its XP file paths and deployment instructions are not generalized to modern systems.


### Claim-level evidence

- **direct** — The .Default profile belongs to LocalSystem and is not the new-user template.
  Section: LocalSystem profile versus template user.
  - [https://devblogs.microsoft.com/oldnewthing/20070302-00/?p=27783/](<https://devblogs.microsoft.com/oldnewthing/20070302-00/?p=27783/>)

### Explanation sources

- [https://devblogs.microsoft.com/oldnewthing/20070302-00/?p=27783/](<https://devblogs.microsoft.com/oldnewthing/20070302-00/?p=27783/>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
