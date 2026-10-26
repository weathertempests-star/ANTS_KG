---
node_id: "knowledge:75cc41a684ac7d7cabc9a294"
generated: true
---

# Config

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\W32Time\Config
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:75cc41a684ac7d7cabc9a294`

## Hierarchy

Parent: [W32Time](knowledge-e5e8c792adda602b0d4e725d.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: time&#95;clock&#95;policy

This machine Windows Time Config policy key contains general and clock-discipline settings, such as thresholds governing abrupt versus gradual clock correction and limits on accepted adjustments. Microsoft describes this policy for domain controllers, including read-only domain controllers. It is separate from provider enablement and NTP peer selection, which reside under the TimeProviders branch rather than being implied by Config.

## Atomic claim

Stores shared Windows Time clock-discipline and general policy parameters.

Scope: **machine**

## Meaning in system-level logs

A registry target here concerns shared time-service policy parameters. Inspect the parameter name, numeric data, operation, and result; observations of clock correction, accepted samples, or synchronization status require Windows Time operational evidence.

### What the path cannot establish

- A Config access does not prove the local clock was changed or synchronized.
- The key does not identify an active NTP peer or whether any configured threshold was reached.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. The policy description specifically addresses domain controllers including RODCs; parameter effects require the relevant Windows Time implementation and service role.


### Claim-level evidence

- **direct** — The policy specifies clock discipline and general W32Time values for domain controllers, including RODCs, and maps to Config.
  Section: W32TIME&#95;POLICY&#95;CONFIG.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;config](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_config>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;config](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_config>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;config](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_config>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
