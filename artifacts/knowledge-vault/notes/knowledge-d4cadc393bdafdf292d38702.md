---
node_id: "knowledge:d4cadc393bdafdf292d38702"
generated: true
---

# Filesystems

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\Filesystems
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:d4cadc393bdafdf292d38702`

## Hierarchy

Parent: [Windows](knowledge-448d4b3e7d83a6ebe3c51a2d.md)

Children:

- [NTFS](knowledge-5a0e50df8a76ec949c0d2710.md)

## Functional explanation

Status: **structural**

Role: filesystem&#95;policy&#95;namespace

This machine Filesystems policy namespace groups the NTFS policy branch documented for selective symbolic-link evaluation. Its function in this inventory is inferred from the NTFS descendant mapping, rather than a universal container for all Windows file-system controls. Other file-system administrative policies can map elsewhere, including System CurrentControlSet locations, so this prefix should not inherit meanings from similarly named registry keys.

## Atomic claim

Groups Windows file-system policy beneath the machine software policy namespace.

Scope: **machine**

## Meaning in system-level logs

A target here locates the file-system policy namespace. Continue to NTFS and the actual setting, with operation, result, and data, to distinguish a policy access from any file-system operation.

### What the path cannot establish

- The namespace does not establish that a symbolic link exists or was followed.
- It does not identify a volume, file, file-system error, or the state of every NTFS feature.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.


### Claim-level evidence

- **structural_inference** — The symbolic-link evaluation policy maps to the NTFS child, supporting the parent grouping role.
  Section: SymlinkEvaluation.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
