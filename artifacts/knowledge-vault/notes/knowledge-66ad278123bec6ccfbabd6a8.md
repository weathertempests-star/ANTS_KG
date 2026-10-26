---
node_id: "knowledge:66ad278123bec6ccfbabd6a8"
generated: true
---

# RESOURCEMAP

## Full prefix

~~~text
HKLM\HARDWARE\RESOURCEMAP
~~~

- Domain: registry
- Depth: L3
- Node ID: `knowledge:66ad278123bec6ccfbabd6a8`

## Hierarchy

Parent: [HARDWARE](knowledge-4b463b0660ae080bd0f6f84a.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: hardware&#95;resource&#95;claims

RESOURCEMAP describes hardware resources claimed by device drivers. This branch belongs to the startup-recreated HARDWARE tree. It supplies context for interpreting resource-related observations, but a particular claim belongs to a specific descendant and its data. Distinguish the registry description of resource use from an observed conflict or operational failure, which requires additional device and driver evidence.

## Atomic claim

RESOURCEMAP describes hardware resources claimed by device drivers.

Scope: **machine**

## Meaning in system-level logs

Resource-map events require the driver-specific path, resource data and boot context to identify the claimed resource.

### What the path cannot establish

- The parent does not prove a resource conflict.
- A recorded claim does not show successful access to the resource.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — ResourceMap describes driver claims on hardware resources.
  Section: Remarks: Hardware / ResourceMap.
  - [https://learn.microsoft.com/en-us/dotnet/api/microsoft.win32.registry.localmachine](<https://learn.microsoft.com/en-us/dotnet/api/microsoft.win32.registry.localmachine>)

### Explanation sources

- [https://learn.microsoft.com/en-us/dotnet/api/microsoft.win32.registry.localmachine](<https://learn.microsoft.com/en-us/dotnet/api/microsoft.win32.registry.localmachine>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/sysinfo/structure-of-the-registry](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/structure-of-the-registry>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
