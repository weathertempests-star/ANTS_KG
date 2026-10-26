---
node_id: "knowledge:3ef5f1fd45140d6e0fdfd82c"
generated: true
---

# System

## Full prefix

~~~text
HKLM\System\CurrentControlSet\Services\EventLog\System
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:3ef5f1fd45140d6e0fdfd82c`

## Hierarchy

Parent: [EventLog](knowledge-89e4e74b89345ca9e5655f84.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: system&#95;event&#95;log&#95;configuration

System is the service-tree configuration branch for the System event log. The System log receives events from operating-system components, including startup failures. The ADMX mapping documents its use for legacy log-access configuration. A reference to this branch therefore concerns system-log settings, not the stored event records. Keep it distinct from the similarly named policy-tree branch and inspect the actual changed data before describing an access-policy change or an effect on log availability.

## Atomic claim

System is the service-tree configuration branch for the System event log.

Scope: **machine**

## Meaning in system-level logs

A System registry event needs the exact entry and SDDL data when access configuration is involved; actual log-read or clear events are separate evidence.

### What the path cannot establish

- The path does not prove the System log was read or cleared.
- The legacy access setting alone does not fully describe modern channel access.

### Applicability

The ADMX CSP lists supported Windows 10 builds with KB5005101 and Windows 11 21H2 onward on specified editions; it distinguishes legacy and modern access settings.


### Claim-level evidence

- **direct** — The legacy System log-access policy maps to this service-tree branch.
  Section: Channel&#95;Log&#95;FileLogAccess&#95;8: ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog>)
- **direct** — The System log receives events from operating-system components, including startup failures.
  Section: Standard logs table: System.
  - [https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key](<https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **HAS_LEGACY_ACCESS_POLICY_COUNTERPART** (incoming): [System](knowledge-f018bde52bb5ae343dd0812f.md)
  Microsoft maps modern System log access policy to the Software Policies location and its corresponding legacy access policy under Services EventLog. They are configuration locations for the same channel, not stores of the event records.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_4>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog>)
- [https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key](<https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;8](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_8>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
