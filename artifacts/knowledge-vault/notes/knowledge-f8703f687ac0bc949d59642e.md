---
node_id: "knowledge:f8703f687ac0bc949d59642e"
generated: true
---

# Security

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\EventLog\Security
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:f8703f687ac0bc949d59642e`

## Hierarchy

Parent: [EventLog](knowledge-8570aba32433b35a4a83423b.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: security&#95;event&#95;log&#95;policy

This machine EventLog Security policy key configures management of the Security event log, including retaining old events, automatic backup, access permissions, and file location. Microsoft distinguishes Security log access from ordinary log access: the documented policy cannot configure write permissions, and both modern and legacy access settings are needed for the corresponding tools. The key stores policy rather than audit records or credentials.

## Atomic claim

Stores administrative policy for Security event-log retention, access, backups, and file location.

Scope: **machine**

## Meaning in system-level logs

Inspect the particular value, SDDL or retention data, operation, and result. To establish auditing gaps, discarded events, a cleared log, or successful log access, examine actual Security channel state and operational evidence.

### What the path cannot establish

- The registry target does not prove an audit event was generated, lost, or cleared.
- Security log read/clear access policy does not imply permission to write Security events.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **AutoBackupLogFiles** (value): Controls automatic backup of a full Security log when retaining old events is enabled.
- **Retention** (value): Controls retaining existing Security events rather than overwriting them when full.

### Claim-level evidence

- **direct** — AutoBackupLogFiles maps here and requires retaining old events.
  Section: Channel&#95;Log&#95;AutoBackup&#95;2.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;autobackup&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_autobackup_2>)
- **direct** — Security log access policy cannot set write permissions and requires corresponding modern and legacy settings.
  Section: Channel&#95;Log&#95;FileLogAccess&#95;2.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_2>)
- **direct** — Retention controls behavior when the Security log reaches maximum size.
  Section: Channel&#95;Log&#95;Retention&#95;2.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;retention&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_retention_2>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **AFFECTS_SAME_EVENT_CHANNEL** (incoming): [Audit](knowledge-cfe58fa3f58d656bd954fcc9.md)
  The Audit command-line setting governs process-creation information emitted to the Security channel when required auditing is enabled; EventLog Security policy separately governs channel file management and access. Neither registry key stores the audit records.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_2>)
- **HAS_LEGACY_ACCESS_POLICY_COUNTERPART** (outgoing): [Security](knowledge-0615018fbc0b36712d73738c.md)
  Microsoft maps modern Security log access policy to the Software Policies location and its corresponding legacy access policy under Services EventLog. They are configuration locations for the same channel, not stores of the event records.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_2>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;autobackup&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_autobackup_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;retention&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_retention_2>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;autobackup&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_autobackup_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;retention&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_retention_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;logfilepath&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_logfilepath_2>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
