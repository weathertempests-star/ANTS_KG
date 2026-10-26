---
node_id: "knowledge:7fb2852e2f15ab5025f4dd0c"
generated: true
---

# Lsa

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Control\Lsa
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:7fb2852e2f15ab5025f4dd0c`

## Hierarchy

Parent: [Control](knowledge-cf70125942441319173f4965.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: local&#95;security&#95;authority&#95;configuration

Lsa contains Local Security Authority configuration including SSP/AP registration. The documented Security Packages entry is a named multi-string value holding package DLL names. It must remain a value of this key in the graph, rather than becoming a fabricated child key. The prefix alone identifies neither one package nor a load event; interpreting a change requires the exact list data and security subsystem context.

## Atomic claim

Lsa contains Local Security Authority configuration including SSP/AP registration.

Scope: **machine**

## Meaning in system-level logs

An Lsa event needs the exact value, old/new data and actor; package-load evidence is needed to establish a successful load.

### What the path cannot establish

- Not every Lsa observation concerns Security Packages.
- A package registration does not establish that loading passed all platform restrictions.

### Applicability

This source documents SSP/AP registration, not every LSA setting or every security-provider mechanism.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **Security Packages** (value): REG&#95;MULTI&#95;SZ list of SSP/AP DLL names without the .dll extension, separated by NUL characters. The documentation distinguishes normal System32 base names from registrations in other directories.

### Claim-level evidence

- **direct** — Security Packages under Lsa registers SSP/AP DLL names.
  Section: Registering SSP/AP DLLs.
  - [https://learn.microsoft.com/en-us/windows/win32/secauthn/registering-ssp-ap-dlls](<https://learn.microsoft.com/en-us/windows/win32/secauthn/registering-ssp-ap-dlls>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/secauthn/registering-ssp-ap-dlls](<https://learn.microsoft.com/en-us/windows/win32/secauthn/registering-ssp-ap-dlls>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/secauthn/registering-ssp-ap-dlls](<https://learn.microsoft.com/en-us/windows/win32/secauthn/registering-ssp-ap-dlls>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
