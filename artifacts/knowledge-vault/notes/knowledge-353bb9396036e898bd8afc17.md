---
node_id: "knowledge:353bb9396036e898bd8afc17"
generated: true
---

# Enum

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Enum
~~~

- Domain: registry
- Depth: L4
- Node ID: `knowledge:353bb9396036e898bd8afc17`

## Hierarchy

Parent: [CurrentControlSet](knowledge-47075c2ddad8552fd6d1728a.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: device&#95;enumeration&#95;namespace

Enum is the operating-system-managed device enumeration registry tree. It supplies device-related state through system interfaces, and Microsoft warns that its internal layout can change. Treat observed descendants as implementation details requiring device context, rather than a stable schema for direct application access. The parent alone cannot identify a newly connected device, a particular driver binding or successful operation of hardware.

## Atomic claim

Enum is the operating-system-managed device enumeration registry tree.

Scope: **machine**

## Meaning in system-level logs

An Enum event needs the device instance path, operation, data and PnP timeline to distinguish enumeration from current device availability.

### What the path cannot establish

- A recorded device entry does not prove the device is presently attached.
- The internal tree layout is not a stable application API contract.

### Applicability

Driver guidance directs consumers to device-property and setup APIs instead of direct Enum access.


### Claim-level evidence

- **direct** — Enum is reserved for operating-system components and its layout is not stable.
  Section: Enum registry tree introduction.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-enum-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-enum-registry-tree>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-enum-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-enum-registry-tree>)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/plug-and-play-registry-routines](<https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/plug-and-play-registry-routines>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-enum-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-enum-registry-tree>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
