---
node_id: "knowledge:57e9c1b0e2c559c40059e2e9"
generated: true
---

# SystemCertificates

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\SystemCertificates
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:57e9c1b0e2c559c40059e2e9`

## Hierarchy

Parent: [Microsoft](knowledge-e80dc586f12d3ed46b0f8a25.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: certificate&#95;policy&#95;store

This machine SystemCertificates policy location contains certificate stores associated with local-machine Group Policy. Windows exposes logical certificate stores by collecting physical stores, including policy-supplied stores where applicable. Microsoft documents this precise registry location and explains that policy stores can be downloaded from Group Policy templates and refreshed after changes. It is a certificate-store location, not a complete account of trust decisions made by applications.

## Atomic claim

Contains the local-machine certificate stores supplied through Group Policy.

Scope: **machine**

## Meaning in system-level logs

A target under this location concerns policy certificate storage. Inspect the store child, certificate identifier or value, registry operation, result, and encoded data to determine the affected material; certificate validation or use needs separate evidence.

### What the path cannot establish

- The parent location does not identify a particular certificate or prove it is trusted for a purpose.
- A registry access does not establish certificate issuance, private-key access, or a TLS connection.

### Applicability

Documented Win32 certificate system-store location on Windows; available logical/physical stores and policy distribution depend on machine configuration, with no single ADMX CSP baseline applying to this API location.


### Claim-level evidence

- **direct** — Microsoft identifies this machine Group Policy certificate-store location and describes template download and change updates.
  Section: CERT&#95;SYSTEM&#95;LOCAL&#95;MACHINE&#95;GROUP&#95;POLICY; Remarks.
  - [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **SUPPLIES_POLICY_CERTIFICATE_STORE** (outgoing): [SystemCertificates](knowledge-1b96f1d311e346ba1fb4b0c9.md)
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
