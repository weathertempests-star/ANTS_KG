---
node_id: "knowledge:5b5b2f915897b9810c4df4e4"
generated: true
---

# &lt;ProductCodeGUID&gt;

## Full prefix

~~~text
HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\<ProductCodeGUID>
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:5b5b2f915897b9810c4df4e4`

## Hierarchy

Parent: [Uninstall](knowledge-4493e53b7f5a42ffe5d1dd0d.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: windows&#95;installer&#95;product&#95;record&#95;template

A product-code GUID child stores Windows Installer metadata for one product. The template identifies the MSI product record shape rather than a concrete installed product. Representative fields describe presentation and servicing information. In particular, an install-date field can be updated by servicing, so it must not be treated as an immutable first-install timestamp. Preserve the actual product code and value data when correlating a software lifecycle event.

## Atomic claim

A product-code GUID child stores Windows Installer metadata for one product.

Scope: **machine**

## Meaning in system-level logs

Retain the actual product GUID, changed field and installer operation; use package/servicing evidence to determine lifecycle meaning.

### What the path cannot establish

- A metadata record does not prove the product is currently functional.
- InstallDate need not represent original installation time.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **DisplayName** (value): Product presentation name derived from ProductName.
- **InstallDate** (value): Last servicing date, or installation date if never repaired or patched.

### Claim-level evidence

- **direct** — Installer properties populate a product-code GUID record.
  Section: Installer-property mapping table.
  - [https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key](<https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key](<https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key](<https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key>)

## Templates and candidate tags

- Placeholder component: true
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
