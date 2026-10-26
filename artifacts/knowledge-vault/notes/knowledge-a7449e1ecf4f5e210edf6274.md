---
node_id: "knowledge:a7449e1ecf4f5e210edf6274"
generated: true
---

# Windows NT

## Full prefix

~~~text
HKCU\Software\Microsoft\Windows NT
~~~

- Domain: registry
- Depth: L4
- Node ID: `knowledge:a7449e1ecf4f5e210edf6274`

## Hierarchy

Parent: [Microsoft](knowledge-774c984f5003cbf507526b35.md)

Children:

- [CurrentVersion](knowledge-175c0719e4dc77467c92b480.md)

## Functional explanation

Status: **structural**

Role: user&#95;windows&#95;nt&#95;namespace

Windows NT is a product-family namespace used by documented per-user Windows configuration, including default-printer management beneath CurrentVersion&#92;Windows. At this parent depth it does not specify a printer, driver, print job, or policy value. Its presence on a modern Windows system reflects a retained registry naming convention rather than evidence that an obsolete Windows NT release is installed or running.

## Atomic claim

Provides the Windows NT namespace above documented per-user Windows preferences.

Scope: **user**

## Meaning in system-level logs

A log at Windows NT alone needs its descendant path and value to identify the feature. Determine the actual Windows release from host metadata rather than the registry branch label.

### What the path cannot establish

- The parent prefix does not specify a child policy value or establish its enabled state.
- An access to this namespace does not prove the descendant feature was used or that a requested change succeeded.

### Applicability

Structural namespace inferred from the cited documented descendants. Each descendant has its own Windows version, feature, and policy-scope requirements.


### Claim-level evidence

- **structural_inference** — The documented default-printer preference path is beneath this parent.
  Section: LegacyDefaultPrinterMode / ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#legacydefaultprintermode](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#legacydefaultprintermode>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#legacydefaultprintermode](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#legacydefaultprintermode>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#legacydefaultprintermode](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#legacydefaultprintermode>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
