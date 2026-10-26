---
node_id: "knowledge:13efa5aa46a334e718e3bb02"
generated: true
---

# DeviceClasses

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Control\DeviceClasses
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:13efa5aa46a334e718e3bb02`

## Hierarchy

Parent: [Control](knowledge-cf70125942441319173f4965.md)

Children:

- [&lt;InterfaceClassGUID&gt;](knowledge-2f9f3274b1f463b66feb0ee8.md)

## Functional explanation

Status: **documented**

Role: device&#95;interface&#95;class&#95;namespace

DeviceClasses groups device interface registrations by interface class. These classes describe functionality exposed to clients, which differs from the installation grouping represented by Control&#92;Class. The parent locates the interface-registration area while concrete GUIDs and instances identify the actual contracts and devices. A registry observation cannot substitute for checking whether an interface instance is enabled and usable at the relevant time.

## Atomic claim

DeviceClasses groups device interface registrations by interface class.

Scope: **machine**

## Meaning in system-level logs

An event here requires the interface-class GUID, instance identifier and operation; correlate device/interface state before describing availability.

### What the path cannot establish

- A device interface class is not the same concept as a setup class.
- Persistent registration does not prove a usable interface is currently enabled.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — DeviceClasses contains a child for each device interface class.
  Section: DeviceClasses.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)
- **direct** — Interface instances require enabling before their names can be used for I/O.
  Section: Overview.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-interface-classes](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-interface-classes>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **DISTINGUISHED_FROM** (incoming): [Class](knowledge-e760864353a1e2b62d9b0831.md)
  Setup classes group installation configuration; interface classes describe exposed device functionality. These are distinct identities.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-setup-classes](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-setup-classes>)
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-interface-classes](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-interface-classes>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-interface-classes](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-interface-classes>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
