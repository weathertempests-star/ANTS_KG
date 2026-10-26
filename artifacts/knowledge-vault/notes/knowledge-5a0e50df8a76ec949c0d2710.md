---
node_id: "knowledge:5a0e50df8a76ec949c0d2710"
generated: true
---

# NTFS

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\Filesystems\NTFS
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:5a0e50df8a76ec949c0d2710`

## Hierarchy

Parent: [Filesystems](knowledge-d4cadc393bdafdf292d38702.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: symbolic&#95;link&#95;evaluation&#95;policy

This machine Filesystems NTFS policy key stores the selective symbolic-link evaluation policy mapped to SymLinkState. Microsoft distinguishes local links to local or remote targets and remote links to local or remote targets. These settings govern following links across those boundaries. They do not describe link creation, grant a symbolic-link creation privilege, or enumerate symbolic links present on a volume.

## Atomic claim

Stores NTFS policy controlling which local and remote symbolic links may be evaluated.

Scope: **machine**

## Meaning in system-level logs

Inspect SymLinkState and associated policy options with the registry operation and result. Actual link traversal needs a file operation identifying the link, resolved target, and outcome; the policy key alone cannot supply them.

### What the path cannot establish

- The key does not show a link was created, evaluated, or blocked.
- It does not grant symbolic-link creation rights or identify the resolved target.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **SymLinkState** (value): Controls policy for selective symbolic-link evaluation; interpretation requires the configured local/remote option data.

### Claim-level evidence

- **direct** — SymLinkState maps here and controls evaluation for four local/remote link and target combinations.
  Section: SymlinkEvaluation.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
