---
node_id: "knowledge:dfe37bea648576cb94eeb5b7"
generated: true
---

# DESCRIPTION

## Full prefix

~~~text
HKLM\HARDWARE\DESCRIPTION
~~~

- Domain: registry
- Depth: L3
- Node ID: `knowledge:dfe37bea648576cb94eeb5b7`

## Hierarchy

Parent: [HARDWARE](knowledge-4b463b0660ae080bd0f6f84a.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: hardware&#95;description&#95;namespace

DESCRIPTION holds descriptive information about the computer hardware. Under the volatile HARDWARE branch, this node narrows an observation to hardware description rather than service-start settings or resource claims. The actual component and property are identified only by descendants and values. Use this as a descriptive namespace in a knowledge graph, without assigning a particular processor, bus or firmware characteristic to the parent.

## Atomic claim

DESCRIPTION holds descriptive information about the computer hardware.

Scope: **machine**

## Meaning in system-level logs

A hardware-description event needs the complete descendant path and value payload to identify the component property.

### What the path cannot establish

- The parent does not establish a particular processor or firmware version.
- The namespace is not a complete historical hardware inventory.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — Description describes actual computer hardware.
  Section: Remarks: Hardware / Description.
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
