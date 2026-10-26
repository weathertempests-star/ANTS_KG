---
node_id: "knowledge:3af0f1159494a70d5b4fc1eb"
generated: true
---

# LocalServer32

## Full prefix

~~~text
HKLM\SOFTWARE\Classes\CLSID\<CLSID>\LocalServer32
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:3af0f1159494a70d5b4fc1eb`

## Hierarchy

Parent: [&lt;CLSID&gt;](knowledge-265a47625042ec0b6ff764f0.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: com&#95;local&#95;server&#95;template

LocalServer32 identifies a local executable COM server registration for a class. Despite its historical name, Microsoft documents server applications of any bitness or architecture. The unnamed value can include arguments, and ServerExecutable can disambiguate the executable. These are activation inputs rather than process history; a registry observation needs the concrete CLSID and value data before it can describe a server-registration change.

## Atomic claim

LocalServer32 identifies a local executable COM server registration for a class.

Scope: **machine**

## Meaning in system-level logs

Preserve CLSID, command-line value, ServerExecutable and registry view; a process-creation record is needed to establish a launch.

### What the path cannot establish

- Registration is not evidence of successful server startup.
- A service-hosted registration can make this launch path inapplicable.

### Applicability

ServerExecutable is documented as supported starting with Windows Server 2003; the general local-server registration supports any architecture.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **(unnamed value)** (value): Executable command line, optionally including application arguments.
- **ServerExecutable** (value): REG&#95;SZ executable path passed separately to process creation.

### Claim-level evidence

- **direct** — LocalServer32 registers executable servers of any architecture.
  Section: Registry entry and Remarks.
  - [https://learn.microsoft.com/en-us/windows/win32/com/localserver32](<https://learn.microsoft.com/en-us/windows/win32/com/localserver32>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/com/localserver32](<https://learn.microsoft.com/en-us/windows/win32/com/localserver32>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/com/localserver32](<https://learn.microsoft.com/en-us/windows/win32/com/localserver32>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
