---
node_id: "knowledge:f0c93ec19e8335644b0de0a8"
generated: true
---

# System

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\System
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:f0c93ec19e8335644b0de0a8`

## Hierarchy

Parent: [Microsoft](knowledge-e80dc586f12d3ed46b0f8a25.md)

Children:

- [DNSClient](knowledge-73129d1644b7f8f197a8c2fb.md)

## Functional explanation

Status: **structural**

Role: dns&#95;suffix&#95;policy&#95;namespace

This machine Microsoft System policy namespace is the parent of the DNSClient branch used for the computer primary DNS suffix policy. Its limited meaning in this inventory is inferred from that child mapping. It should not be treated as a generic replacement for every Windows system setting, nor confused with the separate Policies Microsoft Windows System branch that hosts sign-in and profile controls.

## Atomic claim

Groups the machine primary-DNS-suffix policy under the Microsoft System namespace.

Scope: **machine**

## Meaning in system-level logs

A log target at this parent only locates a policy namespace. The DNSClient child, configured suffix, operation, and result are needed to interpret a primary-DNS-suffix access or change.

### What the path cannot establish

- The parent does not identify the configured DNS suffix.
- It does not show DNS resolution, domain membership, or a successful registration.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.


### Claim-level evidence

- **structural_inference** — The primary DNS suffix policy maps to Software&#92;Policies&#92;Microsoft&#92;System&#92;DNSClient.
  Section: DNS&#95;PrimaryDnsSuffix.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;primarydnssuffix](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_primarydnssuffix>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;primarydnssuffix](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_primarydnssuffix>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;primarydnssuffix](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_primarydnssuffix>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
