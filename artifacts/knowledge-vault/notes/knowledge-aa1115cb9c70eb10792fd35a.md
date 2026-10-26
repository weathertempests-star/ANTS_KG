---
node_id: "knowledge:aa1115cb9c70eb10792fd35a"
generated: true
---

# &lt;LogName&gt;

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Services\EventLog\<LogName>
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:aa1115cb9c70eb10792fd35a`

## Hierarchy

Parent: [EventLog](knowledge-89e4e74b89345ca9e5655f84.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: event&#95;log&#95;configuration&#95;template

A log-name child describes configuration for one event log. The template represents the log identity slot within the EventLog service tree. Representative values describe access control and file location; they are distinct from event sources and actual event records. A real log name and specific setting are needed to interpret a registry access, and stored configuration alone does not reveal event contents or collection success.

## Atomic claim

A log-name child describes configuration for one event log.

Scope: **machine**

## Meaning in system-level logs

Retain actual log name, value name and data; use log-service telemetry to establish whether configuration was applied.

### What the path cannot establish

- The placeholder does not establish that a custom log exists.
- A configuration change does not prove that log data was read, written or cleared.

### Applicability

The source documents the classic Event Logging registry convention and notes the Vista infrastructure redesign.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **CustomSD** (value): SDDL security descriptor for the log in the classic registration contract.
- **File** (value): Location of the backing log file in the documented registration contract.

### Claim-level evidence

- **direct** — Log children contain access and file-location settings.
  Section: Per-log registry values.
  - [https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key](<https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key](<https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key](<https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key>)

## Templates and candidate tags

- Placeholder component: true
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
