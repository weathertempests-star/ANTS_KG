---
node_id: "knowledge:e5e8c792adda602b0d4e725d"
generated: true
---

# W32Time

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\W32Time
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:e5e8c792adda602b0d4e725d`

## Hierarchy

Parent: [Microsoft](knowledge-e80dc586f12d3ed46b0f8a25.md)

Children:

- [Config](knowledge-75cc41a684ac7d7cabc9a294.md)
- [TimeProviders](knowledge-f13a9092b1c4d449908498e2.md)

## Functional explanation

Status: **structural**

Role: time&#95;policy&#95;namespace

This machine W32Time policy namespace groups administrative settings for Windows Time, the service used to maintain clock synchronization. Config contains shared clock-discipline parameters, while TimeProviders separates NTP client behavior from NTP server behavior. The parent role is inferred from documented policy mappings to those descendants. These policy locations are distinct from service runtime configuration and do not themselves record measured clock accuracy.

## Atomic claim

Groups machine policy for Windows Time clock control and NTP providers.

Scope: **machine**

## Meaning in system-level logs

Resolve Config versus the NtpClient or NtpServer provider before interpreting the registry target. Operation, result, and value data distinguish reading clock policy from changing the ability to obtain or serve time.

### What the path cannot establish

- The namespace does not establish that Windows Time is running or synchronized.
- It does not identify the selected time source, clock offset, or an NTP exchange.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.


### Claim-level evidence

- **structural_inference** — Clock discipline and general settings map to Config.
  Section: W32TIME&#95;POLICY&#95;CONFIG.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;config](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_config>)
- **structural_inference** — The input time-synchronization provider maps beneath TimeProviders&#92;NtpClient.
  Section: W32TIME&#95;POLICY&#95;ENABLE&#95;NTPCLIENT.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpclient](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpclient>)
- **structural_inference** — The provider serving time to other computers maps beneath TimeProviders&#92;NtpServer.
  Section: W32TIME&#95;POLICY&#95;ENABLE&#95;NTPSERVER.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpserver>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;config](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_config>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpclient](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpclient>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpserver>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;config](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_config>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;configure&#95;ntpclient](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_configure_ntpclient>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpclient](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpclient>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpserver>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
