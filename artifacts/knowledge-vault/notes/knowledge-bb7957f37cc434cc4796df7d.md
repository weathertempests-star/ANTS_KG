---
node_id: "knowledge:bb7957f37cc434cc4796df7d"
generated: true
---

# Cryptography

## Full prefix

~~~text
HKLM\Software\Microsoft\Cryptography
~~~

- Domain: registry
- Depth: L4
- Node ID: `knowledge:bb7957f37cc434cc4796df7d`

## Hierarchy

Parent: [Microsoft](knowledge-acd43835e6c7c037c564c959.md)

Children:

- [Services](knowledge-71bd47e20b1c0d6281be9b56.md)

## Functional explanation

Status: **structural**

Role: machine&#95;cryptography&#95;namespace

Cryptography groups machine software configuration that includes service certificate-store locations. The verified Services descendant supplies evidence for this containing namespace. The parent is broader than any one service store, so certificate meanings should be assigned only after the full service and SystemCertificates path is known. No universal cryptography option, algorithm or key-material format is defined by this ancestor alone.

## Atomic claim

Cryptography groups machine software configuration that includes service certificate-store locations.

Scope: **machine**

## Meaning in system-level logs

A record here locates a cryptographic subsystem; retain the full descendant, operation and value data before identifying the affected setting.

### What the path cannot establish

- The ancestor alone does not identify a certificate or certificate store.
- The namespace does not establish that any service is running.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **structural_inference** — The service certificate path establishes Cryptography as an ancestor.
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
