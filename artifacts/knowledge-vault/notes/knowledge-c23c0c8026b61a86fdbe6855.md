---
node_id: "knowledge:c23c0c8026b61a86fdbe6855"
generated: true
---

# NtpClient

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\W32time\TimeProviders\NtpClient
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:c23c0c8026b61a86fdbe6855`

## Hierarchy

Parent: [TimeProviders](knowledge-f13a9092b1c4d449908498e2.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: ntp&#95;client&#95;policy

This machine NtpClient policy key controls the Windows Time provider that obtains time from NTP servers. It includes provider enablement and configuration such as time-source names, selection type, and polling or retry parameters. Obtaining time is the client role; the sibling NtpServer provider serves other computers. Configured peer names remain administrative inputs rather than proof that a peer answered or was selected.

## Atomic claim

Configures the Windows NTP client that obtains time for the local clock.

Scope: **machine**

## Meaning in system-level logs

Inspect Enabled or the particular client parameter and its data with operation and result. To determine whether synchronization occurred, correlate with time-service status or events identifying the accepted source, sample, and correction.

### What the path cannot establish

- An Enabled write does not establish successful synchronization or accurate time.
- A configured NTP source is not evidence of a connection, response, or accepted time sample.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **Enabled** (value): Controls enablement of the Windows NTP client provider.

### Claim-level evidence

- **direct** — Configure Windows NTP Client specifies source and timing parameters and maps to this key.
  Section: W32TIME&#95;POLICY&#95;CONFIGURE&#95;NTPCLIENT.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;configure&#95;ntpclient](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_configure_ntpclient>)
- **direct** — The Enabled value controls whether the Windows NTP client can synchronize the computer clock with NTP servers.
  Section: W32TIME&#95;POLICY&#95;ENABLE&#95;NTPCLIENT.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpclient](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpclient>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **COMPLEMENTARY_PROVIDER_ROLE** (outgoing): [NtpServer](knowledge-bec7c2e85f533838168c42fc.md)
  The Windows NTP client obtains time for the local clock, while the NTP server provider answers time requests from other computers; enablement is configured independently.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpclient](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpclient>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpserver>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;configure&#95;ntpclient](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_configure_ntpclient>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpclient](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpclient>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;configure&#95;ntpclient](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_configure_ntpclient>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time&#95;policy&#95;enable&#95;ntpclient](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-w32time#w32time_policy_enable_ntpclient>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
