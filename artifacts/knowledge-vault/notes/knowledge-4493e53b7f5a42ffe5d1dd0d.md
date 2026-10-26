---
node_id: "knowledge:4493e53b7f5a42ffe5d1dd0d"
generated: true
---

# Uninstall

## Full prefix

~~~text
HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:4493e53b7f5a42ffe5d1dd0d`

## Hierarchy

Parent: [CurrentVersion](knowledge-6202b8718fe33a7616eb9084.md)

Children:

- [&lt;ProductCodeGUID&gt;](knowledge-5b5b2f915897b9810c4df4e4.md)

## Functional explanation

Status: **documented**

Role: installed&#95;product&#95;metadata&#95;namespace

Uninstall organizes product registration metadata used for software removal and display. Windows Installer places each product record beneath a product-code GUID. This parent is an inventory and configuration namespace rather than evidence that uninstall has occurred. A specific product record and its values must be examined to identify the software, and the documented MSI layout should not be imposed on every third-party installer.

## Atomic claim

Uninstall organizes product registration metadata used for software removal and display.

Scope: **machine**

## Meaning in system-level logs

An Uninstall event needs the child identity, changed value and installer/process context to distinguish metadata maintenance from removal.

### What the path cannot establish

- The parent does not prove a product was removed.
- Not every child is guaranteed to follow Windows Installer product-code conventions.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — Windows Installer uses product-code child keys beneath Uninstall.
  Section: Registry location and product-code subkey.
  - [https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key](<https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key](<https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key](<https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
