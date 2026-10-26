---
node_id: "knowledge:4b463b0660ae080bd0f6f84a"
generated: true
---

# HARDWARE

## Full prefix

~~~text
HKLM\HARDWARE
~~~

- Domain: registry
- Depth: L2
- Node ID: `knowledge:4b463b0660ae080bd0f6f84a`

## Hierarchy

Parent: [HKLM](knowledge-23067446c79f6f808ec9de07.md)

Children:

- [DESCRIPTION](knowledge-dfe37bea648576cb94eeb5b7.md)
- [DEVICEMAP](knowledge-28ef2eac08d604aee4c71a41.md)
- [RESOURCEMAP](knowledge-66ad278123bec6ccfbabd6a8.md)

## Functional explanation

Status: **documented**

Role: volatile&#95;hardware&#95;information

HARDWARE contains hardware and driver-mapping information rebuilt during system startup. It is a machine branch with descriptive and resource-oriented descendants, distinct from persistent service configuration. Treat observations as information from a particular boot context. A change between two snapshots can reflect rediscovery or driver initialization, so attribution requires the surrounding boot and device timeline rather than a path comparison alone.

## Atomic claim

HARDWARE contains hardware and driver-mapping information rebuilt during system startup.

Scope: **machine**

## Meaning in system-level logs

Hardware records should retain boot/session time, full key, value data and the querying or writing process.

### What the path cannot establish

- The branch is not a durable history of every attached device.
- A snapshot difference does not by itself prove a hardware replacement.

### Applicability

The documentation describes Windows hardware registry organization; driver-class formats and enumerated content vary.


### Claim-level evidence

- **direct** — HARDWARE data is recreated at startup.
  Section: Remarks: Hardware.
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
