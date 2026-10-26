---
node_id: "knowledge:833861c0e2e96ab3dcbe1d65"
generated: true
---

# Current

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Hardware Profiles\Current
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:833861c0e2e96ab3dcbe1d65`

## Hierarchy

Parent: [Hardware Profiles](knowledge-b2df5226b360738770b77f05.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: current&#95;hardware&#95;profile&#95;configuration

Current is the hardware-profile branch exposed through the HKCC predefined key. It locates the current profile-specific configuration within the machine SYSTEM tree. Because HKCC aliases this location, observations through the short and full paths can describe the same underlying data. Preserve the original spelling for provenance while avoiding a false distinction between two independent profile stores. Concrete settings still belong to descendant keys and values.

## Atomic claim

Current is the hardware-profile branch exposed through the HKCC predefined key.

Scope: **machine**

## Meaning in system-level logs

An event at Current should be correlated with HKCC references using the same resolved descendant and operation context.

### What the path cannot establish

- The alias does not create a second independent copy of the configuration.
- The parent does not identify a particular device setting.

### Applicability

Hardware-profile use is deprecated in driver guidance; the alias is still documented.


### Claim-level evidence

- **direct** — HKCC aliases Hardware Profiles Current.
  Section: HKEY&#95;CURRENT&#95;CONFIG.
  - [https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **ALIASES** (incoming): [HKCC](knowledge-1a56d9cce0d016baa90a0134.md)
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
