---
node_id: "knowledge:23bc530a3409aae5c43a7bf5"
generated: true
---

# RunOnce

## Full prefix

~~~text
HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:23bc530a3409aae5c43a7bf5`

## Hierarchy

Parent: [CurrentVersion](knowledge-6202b8718fe33a7616eb9084.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: machine&#95;one&#95;time&#95;logon&#95;commands

RunOnce stores machine-level commands intended for one-time processing at logon. This key has additional execution conditions: the documented machine branch is processed when an administrator logs on after reboot. Value-name prefixes affect deletion timing and Safe Mode handling. The registration therefore cannot be read as an immediate process launch, and removal of a value alone does not demonstrate that its command completed successfully.

## Atomic claim

RunOnce stores machine-level commands intended for one-time processing at logon.

Scope: **machine**

## Meaning in system-level logs

Retain the full value name including prefixes, command data, reboot/logon context and operation result.

### What the path cannot establish

- The key is not a guarantee of execution by every user.
- Value deletion alone does not prove successful completion.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **Named command entries** (value_collection): One-time logon commands; ! defers value deletion, and &#42; changes Safe Mode handling.

### Claim-level evidence

- **direct** — Machine RunOnce has administrator-logon and one-time processing semantics.
  Section: RunOnce restrictions and value prefixes.
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
