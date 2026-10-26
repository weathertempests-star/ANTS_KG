---
node_id: "knowledge:2f9f3274b1f463b66feb0ee8"
generated: true
---

# &lt;InterfaceClassGUID&gt;

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Control\DeviceClasses\<InterfaceClassGUID>
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:2f9f3274b1f463b66feb0ee8`

## Hierarchy

Parent: [DeviceClasses](knowledge-13efa5aa46a334e718e3bb02.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: device&#95;interface&#95;class&#95;template

An interface-class GUID child groups device interfaces that expose a particular functionality. The placeholder represents an interface-class identity within the machine interface tree. It does not name a single hardware device. A class may have several interface instances, so downstream analysis needs the instance path and current state rather than treating a class-level registry observation as a connection or I/O event.

## Atomic claim

An interface-class GUID child groups device interfaces that expose a particular functionality.

Scope: **machine**

## Meaning in system-level logs

Keep the actual interface GUID, instance subpath and state-related event fields to identify the affected interface.

### What the path cannot establish

- The template does not establish any concrete interface instance.
- Class membership alone does not prove recent I/O or device connection.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — Each device interface class has a child in DeviceClasses.
  Section: DeviceClasses.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)
- **direct** — An interface class represents shared device functionality.
  Section: Overview.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-interface-classes](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-interface-classes>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-interface-classes](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-interface-classes>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)

## Templates and candidate tags

- Placeholder component: true
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
