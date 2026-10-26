---
node_id: "knowledge:a59b3ac84eac68e574106e36"
generated: true
---

# RunOnce

## Full prefix

~~~text
HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:a59b3ac84eac68e574106e36`

## Hierarchy

Parent: [CurrentVersion](knowledge-85f2f0739e1a194cea57e654.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: one&#95;time&#95;per&#95;user&#95;logon&#95;command&#95;registration

RunOnce registers commands for a one-time run at user logon rather than recurring launches. Windows normally deletes each entry before executing its command, and special value-name prefixes can alter deletion timing or Safe Mode handling. The location is intended for transient work such as completing setup. Entry creation, disappearance, and command execution are separate observable facts; deletion by itself cannot establish that the intended operation succeeded.

## Atomic claim

Registers commands intended for a one-time logon run for the represented user.

Scope: **user**

## Meaning in system-level logs

Capture the full value name including any exclamation-mark or asterisk prefix, command data, operation, and result. Correlate logon and process records because an entry can be removed before a failed command runs.

### What the path cannot establish

- A missing or deleted entry does not prove successful program execution or setup completion.
- The key name does not establish whether a command is benign, malicious, or newly created.

### Applicability

Documented Windows logon registry convention. The cited article’s administrator-logon restriction is specific to HKLM RunOnce and must not be transferred to this HKCU key.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **Named entries** (value_collection): Application-defined command-line entries; a leading ! defers deletion until after execution and a leading &#42; requests running even in Safe Mode.

### Claim-level evidence

- **direct** — The exact user path, one-time behavior, deletion-before-run default, and special value-name prefixes are documented.
  Section: Run and RunOnce Registry Keys.
  - [https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **ONE_TIME_COUNTERPART_OF** (outgoing): [Run](knowledge-133870b9f8825b6703ab5724.md)
  Both configure user-logon command launches, but RunOnce has one-time entry processing and deletion semantics whereas Run entries recur at logon.
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
