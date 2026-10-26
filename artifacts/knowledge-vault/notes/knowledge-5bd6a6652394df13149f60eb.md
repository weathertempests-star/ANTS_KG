---
node_id: "knowledge:5bd6a6652394df13149f60eb"
generated: true
---

# Run

## Full prefix

~~~text
HKLM\Software\Microsoft\Windows\CurrentVersion\Run
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:5bd6a6652394df13149f60eb`

## Hierarchy

Parent: [CurrentVersion](knowledge-6202b8718fe33a7616eb9084.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: machine&#95;logon&#95;run&#95;commands

Run stores machine-level command registrations intended for repeated user-logon execution. Its named values hold command lines, not child keys for each executable. The location expresses a startup registration mechanism rather than proof that a command ran. Observations should retain the value name and full command data and be correlated with a qualifying logon and process evidence before describing an execution outcome.

## Atomic claim

Run stores machine-level command registrations intended for repeated user-logon execution.

Scope: **machine**

## Meaning in system-level logs

A Run event needs the value name, old/new command data, actor and operation; correlate logon and process creation separately.

### What the path cannot establish

- A registration write does not prove command execution.
- The key does not guarantee execution order or prompt launch time.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **Named command entries** (value_collection): Each value pairs a descriptive name with a logon command line.

### Claim-level evidence

- **direct** — Run registers commands for repeated logon execution.
  Section: Run and RunOnce behavior.
  - [https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
