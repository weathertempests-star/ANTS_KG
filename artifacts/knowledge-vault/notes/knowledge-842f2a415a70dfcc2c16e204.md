---
node_id: "knowledge:842f2a415a70dfcc2c16e204"
generated: true
---

# &lt;SetupClassGUID&gt;

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Control\Class\<SetupClassGUID>
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:842f2a415a70dfcc2c16e204`

## Hierarchy

Parent: [Class](knowledge-e760864353a1e2b62d9b0831.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: device&#95;setup&#95;class&#95;template

A setup-class GUID child contains configuration shared by one device setup class. The template is the slot for a class identity, not an actual device or driver on a host. Class-level configuration can affect more than one member device. Interpret the concrete GUID and changed setting together, and keep it separate from the interface-class GUID used to describe an I/O contract.

## Atomic claim

A setup-class GUID child contains configuration shared by one device setup class.

Scope: **machine**

## Meaning in system-level logs

Retain the concrete setup GUID, value name/data and installation actor when interpreting class configuration changes.

### What the path cannot establish

- The placeholder does not establish that a concrete class exists on the host.
- A class registration cannot establish that an individual device is present.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — Each Class GUID child contains information for one setup class.
  Section: Class.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)
- **direct** — Setup-class settings can be common to member devices.
  Section: Overview.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-setup-classes](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-setup-classes>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-setup-classes](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-setup-classes>)

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
