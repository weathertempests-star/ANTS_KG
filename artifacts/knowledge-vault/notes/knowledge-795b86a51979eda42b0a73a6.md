---
node_id: "knowledge:795b86a51979eda42b0a73a6"
generated: true
---

# CoDeviceInstallers

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Control\CoDeviceInstallers
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:795b86a51979eda42b0a73a6`

## Hierarchy

Parent: [Control](knowledge-cf70125942441319173f4965.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: class&#95;coinstaller&#95;registrations

CoDeviceInstallers contains registrations for class-specific device coinstallers. The node belongs to device-installation configuration beneath Control. It identifies registration metadata, not an execution record or the installation of a particular device. Use the actual entry and installation context to determine the responsible class and component. No generic schema for every coinstaller value is assumed from the parent description.

## Atomic claim

CoDeviceInstallers contains registrations for class-specific device coinstallers.

Scope: **machine**

## Meaning in system-level logs

A coinstaller-registry event needs the concrete entry, data, installer process and target setup class.

### What the path cannot establish

- Registration does not prove that a coinstaller was invoked.
- The parent does not identify a specific class or device.

### Applicability

This is the documented class-coinstaller namespace; applicability depends on the driver package model and installation mechanism in use. Microsoft marks class installers and co-installers deprecated; this does not establish a universal release where this key ceased to exist.


### Claim-level evidence

- **direct** — CoDeviceInstallers records class-specific coinstaller registrations.
  Section: CoDeviceInstallers.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)
- **direct** — Class installers and co-installers are deprecated.
  Section: Note.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/specific-requirements-for-device-property-page-providers--class-instal](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/specific-requirements-for-device-property-page-providers--class-instal>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/specific-requirements-for-device-property-page-providers--class-instal](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/specific-requirements-for-device-property-page-providers--class-instal>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
