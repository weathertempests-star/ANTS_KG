---
node_id: "knowledge:939af1ce2ee8f202f9fc1162"
generated: true
---

# Microsoft

## Full prefix

~~~text
HKU\<UserHive>\Software\Microsoft
~~~

- Domain: registry
- Depth: L4
- Node ID: `knowledge:939af1ce2ee8f202f9fc1162`

## Hierarchy

Parent: [Software](knowledge-9c1888fb225c292950b4d253.md)

Children:

- [SystemCertificates](knowledge-1601525fd6feca8afbd33b39.md)

## Functional explanation

Status: **structural**

Role: user&#95;microsoft&#95;namespace&#95;template

Microsoft selects a vendor grouping within a selected user hive’s software configuration. The documented SystemCertificates child provides one verified facility beneath this vendor prefix. This layer narrows the software owner while leaving the feature unresolved; it is not itself a certificate store or a particular application. Keep the user-hive identity and next subsystem component when interpreting an access.

## Atomic claim

Microsoft selects a vendor grouping within a selected user hive’s software configuration.

Scope: **user**

## Meaning in system-level logs

A record here concerns a Microsoft-owned configuration namespace in the resolved user hive. The subsystem child, operation and value data are necessary to identify its functional target.

### What the path cannot establish

- The ancestor does not identify a specific certificate or store.
- The placeholder does not prove a particular user profile is loaded.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **structural_inference** — The documented per-user certificate path establishes this ancestor.
  Section: CERT&#95;SYSTEM&#95;STORE&#95;USERS.
  - [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
