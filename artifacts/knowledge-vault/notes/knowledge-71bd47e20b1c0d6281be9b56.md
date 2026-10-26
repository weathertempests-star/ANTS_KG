---
node_id: "knowledge:71bd47e20b1c0d6281be9b56"
generated: true
---

# Services

## Full prefix

~~~text
HKLM\Software\Microsoft\Cryptography\Services
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:71bd47e20b1c0d6281be9b56`

## Hierarchy

Parent: [Cryptography](knowledge-bb7957f37cc434cc4796df7d.md)

Children:

- [&lt;ServiceName&gt;](knowledge-171ff28762bc174c62409a83.md)

## Functional explanation

Status: **structural**

Role: service&#95;certificate&#95;namespace

Services organizes service-specific certificate configuration under Cryptography. Its service-named children lead to SystemCertificates locations. This namespace is distinct from SYSTEM&#92;CurrentControlSet&#92;Services, which organizes service and driver configuration. The shared word Services does not make the two trees equivalent. A concrete service identifier and the store descendant are required before a record can be associated with one service certificate collection.

## Atomic claim

Services organizes service-specific certificate configuration under Cryptography.

Scope: **machine**

## Meaning in system-level logs

A record here locates a service certificate namespace; retain the full descendant, operation and value data before identifying the affected setting.

### What the path cannot establish

- The ancestor alone does not identify a certificate or certificate store.
- The namespace does not establish that any service is running.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **structural_inference** — Service certificate paths place named services below Cryptography Services.
  Section: CERT&#95;SYSTEM&#95;STORE&#95;SERVICES.
  - [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
