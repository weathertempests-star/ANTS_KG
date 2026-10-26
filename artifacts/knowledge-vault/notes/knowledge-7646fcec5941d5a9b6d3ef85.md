---
node_id: "knowledge:7646fcec5941d5a9b6d3ef85"
generated: true
---

# Session Manager

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Control\Session Manager
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:7646fcec5941d5a9b6d3ef85`

## Hierarchy

Parent: [Control](knowledge-cf70125942441319173f4965.md)

Children:

- [Environment](knowledge-67ee8ba9716dc0d7a0e5161f.md)

## Functional explanation

Status: **documented**

Role: session&#95;manager&#95;configuration

Session Manager is the configuration namespace for Windows session-manager-related system initialization settings. Its contents include the Environment subkey for system environment variables and the PendingFileRenameOperations value used to record file rename or deletion work deferred until restart. The node identifies the containing key; those subkeys and named values are distinct objects with their own semantics. Reading this path alone does not reveal their configured data or establish that any deferred work occurred.

## Atomic claim

Session Manager contains system initialization configuration, including deferred file operations.

Scope: **machine**

## Meaning in system-level logs

Retain the named value and full multi-string data for deferred operations; Environment-child accesses require variable-level interpretation.

### What the path cannot establish

- A deferred request is not proof the file was renamed or deleted.
- The parent does not imply that every access changes startup behavior.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **PendingFileRenameOperations** (value): REG&#95;MULTI&#95;SZ data encoding file renames or deletions requested for restart.
- **Environment** (subkey): Child containing system environment-variable definitions.

### Claim-level evidence

- **direct** — PendingFileRenameOperations records deferred restart-time rename or deletion requests.
  Section: Remarks: MOVEFILE&#95;DELAY&#95;UNTIL&#95;REBOOT.
  - [https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexa](<https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexa>)
- **direct** — System variables map to Session Manager Environment.
  Section: Name property MappingStrings.
  - [https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment](<https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexa](<https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexa>)
- [https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment](<https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexa](<https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexa>)
- [https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment](<https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
