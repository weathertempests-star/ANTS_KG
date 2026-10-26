---
node_id: "knowledge:9fc16c2f9b1242a4650eb580"
generated: true
---

# SystemCertificates

## Full prefix

~~~text
HKCU\Software\Microsoft\SystemCertificates
~~~

- Domain: registry
- Depth: L4
- Node ID: `knowledge:9fc16c2f9b1242a4650eb580`

## Hierarchy

Parent: [Microsoft](knowledge-774c984f5003cbf507526b35.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: current&#95;user&#95;certificate&#95;store&#95;location

This key is the documented registry location for certificate system stores opened at CERT&#95;SYSTEM&#95;STORE&#95;CURRENT&#95;USER. Named system stores beneath it combine physical sibling stores through the certificate store provider, so the parent is a store-location namespace rather than one certificate or one trust decision. Certificate placement, logical store membership, and certificate validation are related but separate facts that require the actual descendant store and certificate properties.

## Atomic claim

Locates the current user’s certificate system stores.

Scope: **user**

## Meaning in system-level logs

Identify the descendant store and certificate record, operation, result, and account SID in certificate-related registry logs. A parent-key read or write cannot determine whether a particular certificate became trusted or was used in authentication.

### What the path cannot establish

- This location alone does not identify a certificate, private key, or certification authority.
- Store presence does not establish certificate validity, trust-chain success, or private-key possession.

### Applicability

Windows CryptoAPI system-store model. The selected store location, store name, physical stores, and caller context determine the concrete certificate collection.


### Claim-level evidence

- **direct** — Microsoft locates current-user system stores here and describes the logical collection of physical stores.
  Section: CERT&#95;SYSTEM&#95;STORE&#95;CURRENT&#95;USER; opening system stores.
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
