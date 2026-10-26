---
node_id: "knowledge:67ee8ba9716dc0d7a0e5161f"
generated: true
---

# Environment

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:67ee8ba9716dc0d7a0e5161f`

## Hierarchy

Parent: [Session Manager](knowledge-7646fcec5941d5a9b6d3ef85.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: system&#95;environment&#95;configuration

Environment stores system-level environment-variable definitions under the active system configuration. Individual named values represent variables and their configured data. This key identifies the machine-level environment configuration namespace; it is distinct from a particular process environment, which may include inherited, expanded, or process-local values.

## Atomic claim

Environment stores machine-level environment-variable definitions.

Scope: **machine**

## Meaning in system-level logs

An environment event needs the variable name, type, data and process/restart timing to relate persisted configuration to a process environment.

### What the path cannot establish

- Persisted definitions do not prove an existing process has refreshed its environment.
- The parent does not show the effective expanded value of a variable in one process.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **Variable-name entries** (value_collection): Named values define persistent system environment variables.

### Claim-level evidence

- **direct** — System environment variables map to Session Manager Environment.
  Section: Name and SystemVariable properties.
  - [https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment](<https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **CONTRASTS_MACHINE_AND_USER_SCOPE** (outgoing): [Environment](knowledge-c03c4329e2273c4634c1e2bb.md)
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
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
