---
node_id: "knowledge:bec7c2e85f533838168c42fc"
generated: true
---

# NtpServer

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\W32Time\TimeProviders\NtpServer
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:bec7c2e85f533838168c42fc`

## Hierarchy

Parent: [TimeProviders](knowledge-f13a9092b1c4d449908498e2.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: ntp&#95;server&#95;policy

This machine NtpServer policy key controls the Windows Time provider that can answer NTP requests from other computers. Microsoft maps the Enable Windows NTP Server policy to its Enabled value. The server role supplies time to peers and is separate from the NtpClient role that obtains time locally. Enabling a provider does not establish that listeners are reachable or that the supplied clock is accurate.

## Atomic claim

Controls the Windows NTP server provider that answers other computers time requests.

Scope: **machine**

## Meaning in system-level logs

An access to Enabled here concerns serving time, rather than selecting an upstream source. Use the registry operation, result, and data, and require separate network or service evidence to establish whether a request was answered.

### What the path cannot establish

- Provider configuration does not prove the machine answered any NTP request.
- The path does not establish upstream synchronization, network reachability, or time accuracy.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **Enabled** (value): Controls enablement of the Windows NTP server provider.

### Claim-level evidence

- **direct** — The Enabled value maps here; enabling the policy permits serving NTP requests from other computers.
  Section: W32TIME&#95;POLICY&#95;ENABLE&#95;NTPSERVER.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpserver>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **COMPLEMENTARY_PROVIDER_ROLE** (incoming): [NtpClient](knowledge-c23c0c8026b61a86fdbe6855.md)
  The Windows NTP client obtains time for the local clock, while the NTP server provider answers time requests from other computers; enablement is configured independently.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpclient](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpclient>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpserver>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpserver>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpserver>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
