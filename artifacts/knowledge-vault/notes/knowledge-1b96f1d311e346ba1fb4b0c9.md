---
node_id: "knowledge:1b96f1d311e346ba1fb4b0c9"
generated: true
---

# SystemCertificates

## Full prefix

~~~text
HKLM\Software\Microsoft\SystemCertificates
~~~

- Domain: registry
- Depth: L4
- Node ID: `knowledge:1b96f1d311e346ba1fb4b0c9`

## Hierarchy

Parent: [Microsoft](knowledge-acd43835e6c7c037c564c959.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: machine&#95;certificate&#95;store&#95;namespace

SystemCertificates locates machine certificate system-store data. The node supplies machine scope for certificate collections, with actual stores below it. It is not one certificate, private key or universal trust decision. Because system stores can aggregate physical stores, interpretation should retain the named store and certificate identity and distinguish stored material from the chain-policy result for a particular application.

## Atomic claim

SystemCertificates locates machine certificate system-store data.

Scope: **machine**

## Meaning in system-level logs

A machine-certificate event needs the store child, certificate identifier, operation and resulting data to identify the material affected.

### What the path cannot establish

- The parent does not mean a certificate is in the trusted-root store.
- Stored certificate material alone does not demonstrate successful validation.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — Machine certificate stores use HKLM Software Microsoft SystemCertificates.
  Section: CERT&#95;SYSTEM&#95;STORE&#95;LOCAL&#95;MACHINE.
  - [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **SUPPLIES_POLICY_CERTIFICATE_STORE** (incoming): [SystemCertificates](knowledge-57e9c1b0e2c559c40059e2e9.md)
  The machine certificate system stores can include Group Policy physical stores, whose documented policy registry location is separate from the ordinary machine certificate location. This relationship does not establish trust in an individual certificate.
  - [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
