---
node_id: "knowledge:1a56d9cce0d016baa90a0134"
generated: true
---

# HKCC

## Full prefix

~~~text
HKCC
~~~

- Domain: registry
- Depth: L1
- Node ID: `knowledge:1a56d9cce0d016baa90a0134`

## Hierarchy

Parent: Root

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: current&#95;hardware&#95;profile&#95;view

HKCC is the predefined view of the current hardware profile. It aliases HKLM&#92;SYSTEM&#92;CurrentControlSet&#92;Hardware Profiles&#92;Current. Its purpose is to expose profile-specific differences from the standard machine configuration. Interpret this root as an access view: the same configuration may appear under its full machine path, and this name alone does not identify a physical device or a changed setting.

## Atomic claim

HKCC is the predefined view of the current hardware profile.

Scope: **logical_view**

## Meaning in system-level logs

A record naming HKCC concerns the current hardware-profile view; retain the resolved full path, requested operation and process context.

### What the path cannot establish

- The root does not identify a particular device.
- A reference through HKCC and its machine alias need not represent two changes.

### Applicability

Hardware profiles are deprecated in current driver guidance; this alias remains documented.


### Claim-level evidence

- **direct** — HKCC aliases the current hardware-profile branch.
  Section: HKEY&#95;CURRENT&#95;CONFIG.
  - [https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **ALIASES** (outgoing): [Current](knowledge-833861c0e2e96ab3dcbe1d65.md)
  HKCC is the predefined alias of the current hardware-profile branch.
  - [https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys>)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-hardwareprofiles-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-hardwareprofiles-registry-tree>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
