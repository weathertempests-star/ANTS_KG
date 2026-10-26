---
node_id: "knowledge:28ef2eac08d604aee4c71a41"
generated: true
---

# DEVICEMAP

## Full prefix

~~~text
HKLM\HARDWARE\DEVICEMAP
~~~

- Domain: registry
- Depth: L3
- Node ID: `knowledge:28ef2eac08d604aee4c71a41`

## Hierarchy

Parent: [HARDWARE](knowledge-4b463b0660ae080bd0f6f84a.md)

Children:

- [VIDEO](knowledge-b565920c9993486bd27c6f11.md)

## Functional explanation

Status: **documented**

Role: driver&#95;device&#95;mapping&#95;namespace

DEVICEMAP groups hardware mapping data whose layout depends on the driver class. Its position under HARDWARE distinguishes the mappings from the persistent registration of a service under SYSTEM. Different children can represent different device classes, so the parent has no universal value schema. An analyst must resolve the child class and consult its contract before interpreting the data as a device identifier or driver association.

## Atomic claim

DEVICEMAP groups hardware mapping data whose layout depends on the driver class.

Scope: **machine**

## Meaning in system-level logs

A device-mapping record requires its class-specific child path, value name, data type and boot context.

### What the path cannot establish

- No universal value schema can be assigned to this parent.
- A mapping alone does not demonstrate successful device I/O.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — DeviceMap data formats are driver-class-specific.
  Section: Remarks: Hardware / DeviceMap.
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
