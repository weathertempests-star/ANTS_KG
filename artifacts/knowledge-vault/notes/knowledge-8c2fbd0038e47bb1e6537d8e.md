---
node_id: "knowledge:8c2fbd0038e47bb1e6537d8e"
generated: true
---

# Classes

## Full prefix

~~~text
HKCU\Software\Classes
~~~

- Domain: registry
- Depth: L3
- Node ID: `knowledge:8c2fbd0038e47bb1e6537d8e`

## Hierarchy

Parent: [Software](knowledge-86ce335845d887ebaaec150e.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: per&#95;user&#95;class&#95;registration&#95;store

This key stores the current user’s class-registration information used in the merged HKEY&#95;CLASSES&#95;ROOT view, including relevant COM and shell registration namespaces. Windows combines eligible per-user entries here with machine-wide entries under HKLM&#92;Software&#92;Classes according to documented merge rules. The physical user branch and the merged logical view are distinct, and COM configuration selection can also depend on elevation and User Account Control behavior.

## Atomic claim

Stores per-user class registrations that contribute to the HKEY&#95;CLASSES&#95;ROOT merged view.

Scope: **user**

## Meaning in system-level logs

For a log here, preserve the actual registration child, user SID, value data, and process elevation context. Compare the machine registration and merged view when determining which registration a consumer would resolve.

### What the path cannot establish

- A parent-key access does not identify a COM server, file association, or registered executable.
- A stored registration does not prove activation, execution, or malicious hijacking.

### Applicability

Windows class-registration model; the cited documentation distinguishes modern elevation/UAC behavior from Windows XP/Server 2003 behavior.


### Claim-level evidence

- **direct** — The merged view combines HKCU and HKLM Software&#92;Classes subject to explicit duplicate-handling and COM elevation conditions.
  Section: Merged View of HKEY&#95;CLASSES&#95;ROOT.
  - [https://learn.microsoft.com/en-us/windows/win32/sysinfo/merged-view-of-hkey-classes-root](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/merged-view-of-hkey-classes-root>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **CONTRIBUTES_TO_MERGED_VIEW** (outgoing): [HKCR](knowledge-8676a23f044533833c4be696.md)
  Windows merges eligible per-user class registrations with HKLM class registrations in the logical HKEY&#95;CLASSES&#95;ROOT view according to documented duplicate-handling rules.
  - [https://learn.microsoft.com/en-us/windows/win32/sysinfo/merged-view-of-hkey-classes-root](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/merged-view-of-hkey-classes-root>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/sysinfo/merged-view-of-hkey-classes-root](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/merged-view-of-hkey-classes-root>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
