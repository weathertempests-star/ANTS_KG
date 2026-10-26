---
node_id: "knowledge:e42363b508bdb25cfd5079fd"
generated: true
---

# SystemCertificates

## Full prefix

~~~text
HKCU\Software\Policies\Microsoft\SystemCertificates
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:e42363b508bdb25cfd5079fd`

## Hierarchy

Parent: [Microsoft](knowledge-84a535c5fdfd000f10ca6203.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;group&#95;policy&#95;certificate&#95;store&#95;location

This key is the documented current-user Group Policy certificate-store location, separate from the ordinary current-user certificate-store branch under Software&#92;Microsoft. Microsoft describes policy stores as receiving certificate material from the Group Policy Template during startup or logon and being updateable after policy changes. The parent identifies the policy store location; the actual descendant store and certificate records determine which certificate data is present.

## Atomic claim

Locates certificate system stores supplied through user Group Policy.

Scope: **user**

## Meaning in system-level logs

A log here can concern policy certificate-store access or maintenance. Retain the user SID, store suffix, certificate record, value data, operation, and policy-refresh context before interpreting an observed modification.

### What the path cannot establish

- The policy path does not identify the originating domain controller or prove that Group Policy performed the logged write.
- A certificate record does not prove a successful trust decision, authentication, or possession of its private key.

### Applicability

Windows CryptoAPI user Group Policy store location; domain delivery descriptions apply when the client participates in the documented network Group Policy configuration.


### Claim-level evidence

- **direct** — Microsoft gives this user-policy registry location and explains policy store delivery from the Group Policy Template.
  Section: CERT&#95;SYSTEM&#95;CURRENT&#95;USER&#95;GROUP&#95;POLICY; Remarks.
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
