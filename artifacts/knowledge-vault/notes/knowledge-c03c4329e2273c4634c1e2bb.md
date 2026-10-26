---
node_id: "knowledge:c03c4329e2273c4634c1e2bb"
generated: true
---

# Environment

## Full prefix

~~~text
HKU\<UserHive>\Environment
~~~

- Domain: registry
- Depth: L3
- Node ID: `knowledge:c03c4329e2273c4634c1e2bb`

## Hierarchy

Parent: [&lt;UserHive&gt;](knowledge-c7c879f8a0c5cbdfbd6f5a91.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;environment&#95;template

Environment stores persistent environment-variable definitions for the selected user hive. This node is scoped by the actual UserHive ancestor and is distinct from machine environment configuration under Session Manager. A value change updates stored profile configuration, while a process has its own effective environment. To explain an event, retain the variable name and data and establish which user hive and process lifetime are involved.

## Atomic claim

Environment stores persistent environment-variable definitions for the selected user hive.

Scope: **user**

## Meaning in system-level logs

A user-environment event needs the concrete hive identity, variable name, data and process creation context.

### What the path cannot establish

- The template does not identify the current interactive user.
- A write does not prove an already running process adopted the new value.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **Variable-name entries** (value_collection): Named entries define persistent environment variables for this user hive.

### Claim-level evidence

- **direct** — Win32&#95;Environment queries per-user variables from this path.
  Section: Introduction: HKEY&#95;USERS user Environment.
  - [https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment](<https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **CONTRASTS_MACHINE_AND_USER_SCOPE** (incoming): [Environment](knowledge-67ee8ba9716dc0d7a0e5161f.md)
  The WMI environment documentation separates system variables from per-user hive variables.
  - [https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment](<https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment](<https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment](<https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
