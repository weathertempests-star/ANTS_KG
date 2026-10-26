---
node_id: "knowledge:971c29595808f7a4b70fee7a"
generated: true
---

# FileSystem

## Full prefix

~~~text
HKLM\System\CurrentControlSet\Control\FileSystem
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:971c29595808f7a4b70fee7a`

## Hierarchy

Parent: [Control](knowledge-cf70125942441319173f4965.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: filesystem&#95;configuration

FileSystem contains system file-system configuration, including the Win32 long-path opt-in setting. Its location under Control identifies a system facility, while individual value names determine the relevant behavior. Long-path support is conditional on the consuming application and API, so this key alone cannot establish that an arbitrary program accepts longer paths. Keep registry configuration separate from the success or failure of a particular file operation.

## Atomic claim

FileSystem contains system file-system configuration, including the Win32 long-path opt-in setting.

Scope: **machine**

## Meaning in system-level logs

A FileSystem event needs value name, type, old/new data and process lifetime context; for long paths also check application manifest and API use.

### What the path cannot establish

- LongPathsEnabled alone does not remove limits from every application.
- A setting write does not prove a long-path file operation succeeded.

### Applicability

The documented long-path opt-in begins with Windows 10 version 1607; CSP delivery has its own later applicability table.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **LongPathsEnabled** (value): REG&#95;DWORD 1 participates in long-path opt-in for applications declaring longPathAware.

### Claim-level evidence

- **direct** — FileSystem LongPathsEnabled participates in the per-application long-path opt-in.
  Section: Registry setting to enable long paths.
  - [https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation](<https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation](<https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#longpathsenabled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#longpathsenabled>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
