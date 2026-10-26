---
node_id: "knowledge:73129d1644b7f8f197a8c2fb"
generated: true
---

# DNSClient

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\System\DNSClient
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:73129d1644b7f8f197a8c2fb`

## Hierarchy

Parent: [System](knowledge-f0c93ec19e8335644b0de0a8.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: primary&#95;dns&#95;suffix&#95;policy

This machine Microsoft System DNSClient policy key stores the primary DNS suffix setting used in the computer full DNS name. Microsoft documents that the policy can override the suffix configured through System properties. This exact location concerns the computer primary suffix; the separate Windows NT DNSClient policy key hosts other resolver, connection-suffix, and dynamic-registration controls.

## Atomic claim

Stores policy for the computer primary DNS suffix.

Scope: **machine**

## Meaning in system-level logs

For an access here, inspect the actual suffix-setting data with operation and result. A registry update can concern the computer naming configuration, while a DNS query or registration must be demonstrated through separate resolver or network evidence.

### What the path cannot establish

- A key reference alone does not identify the configured primary suffix.
- The path does not prove domain join, successful DNS resolution, or registration of a host record.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.


### Claim-level evidence

- **direct** — DNS&#95;PrimaryDnsSuffix maps here and supersedes the primary DNS suffix configured using System Control Panel.
  Section: DNS&#95;PrimaryDnsSuffix.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;primarydnssuffix](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_primarydnssuffix>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **COMPLEMENTARY_DNS_POLICY_LOCATION** (outgoing): [DNSClient](knowledge-d147cfaf2958552b80b46fbf.md)
  Microsoft System DNSClient hosts the computer primary DNS suffix policy; Windows NT DNSClient hosts distinct DNS server, connection-specific suffix, registration, and resolver policies.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;primarydnssuffix](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_primarydnssuffix>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;domain](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_domain>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;nameserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_nameserver>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;primarydnssuffix](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_primarydnssuffix>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;primarydnssuffix](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_primarydnssuffix>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
