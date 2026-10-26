---
node_id: "knowledge:f018bde52bb5ae343dd0812f"
generated: true
---

# System

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\EventLog\System
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:f018bde52bb5ae343dd0812f`

## Hierarchy

Parent: [EventLog](knowledge-8570aba32433b35a4a83423b.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: system&#95;event&#95;log&#95;policy

This machine EventLog System policy key configures the System event log through policies for file location, access, retention, and automatic backup. It concerns how the Event Log service manages this channel, not the records emitted by drivers or services. Microsoft maps modern permissions here and legacy access separately; retaining old events and automatically backing up full logs are distinct, interacting choices.

## Atomic claim

Stores administrative policies for System event-log file management and access.

Scope: **machine**

## Meaning in system-level logs

Inspect the exact value, configured data, registry operation, and result. A System log policy access does not report a system error, service start, event clear, or file backup; those need separate evidence.

### What the path cannot establish

- No actual System event or service failure is established by this path.
- A retention or backup configuration does not demonstrate rollover, backup, or discarded events.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **AutoBackupLogFiles** (value): Controls automatic backup of a full System log when retention is enabled.
- **Retention** (value): Controls full System log retention behavior.

### Claim-level evidence

- **direct** — AutoBackupLogFiles maps to System and depends on retention.
  Section: Channel&#95;Log&#95;AutoBackup&#95;4.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;autobackup&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_autobackup_4>)
- **direct** — System log access uses SDDL and corresponding modern/legacy settings.
  Section: Channel&#95;Log&#95;FileLogAccess&#95;4.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_4>)
- **direct** — Retention controls whether full-log writes discard new events or overwrite old ones.
  Section: Channel&#95;Log&#95;Retention&#95;4.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;retention&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_retention_4>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **HAS_LEGACY_ACCESS_POLICY_COUNTERPART** (outgoing): [System](knowledge-3ef5f1fd45140d6e0fdfd82c.md)
  Microsoft maps modern System log access policy to the Software Policies location and its corresponding legacy access policy under Services EventLog. They are configuration locations for the same channel, not stores of the event records.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_4>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;autobackup&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_autobackup_4>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_4>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;retention&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_retention_4>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;autobackup&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_autobackup_4>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_4>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;retention&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_retention_4>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;logfilepath&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_logfilepath_4>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
