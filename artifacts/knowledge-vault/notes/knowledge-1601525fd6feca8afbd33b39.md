---
node_id: "knowledge:1601525fd6feca8afbd33b39"
generated: true
---

# SystemCertificates

## Full prefix

~~~text
HKU\<UserHive>\Software\Microsoft\SystemCertificates
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:1601525fd6feca8afbd33b39`

## Hierarchy

Parent: [Microsoft](knowledge-939af1ce2ee8f202f9fc1162.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;certificate&#95;store&#95;template

SystemCertificates locates certificate system stores for the selected user hive. The parent identity determines which user context owns the location. Actual stores and certificate material are represented below it; the node is neither one certificate nor a guarantee of trusted status. Because system stores are logical collections, a registry view alone is insufficient to characterize every effective physical store or an application-specific chain-validation outcome.

## Atomic claim

SystemCertificates locates certificate system stores for the selected user hive.

Scope: **user**

## Meaning in system-level logs

A user-certificate event needs the concrete hive, named store, certificate identifier and operation result.

### What the path cannot establish

- The template does not prove a user certificate exists.
- The parent does not establish that a stored certificate is trusted or currently valid.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — User certificate stores use the user-hive SystemCertificates path.
  Section: CERT&#95;SYSTEM&#95;STORE&#95;USERS.
  - [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
