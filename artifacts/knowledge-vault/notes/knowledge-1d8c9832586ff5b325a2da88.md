---
node_id: "knowledge:1d8c9832586ff5b325a2da88"
generated: true
---

# Application

## Full prefix

~~~text
HKLM\System\CurrentControlSet\Services\EventLog\Application
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:1d8c9832586ff5b325a2da88`

## Hierarchy

Parent: [EventLog](knowledge-89e4e74b89345ca9e5655f84.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: application&#95;event&#95;log&#95;configuration

Application is the service-tree configuration branch for the Application event log. The Application log receives events chosen by applications. The ADMX mapping documents its use for legacy log-access configuration. A reference to this branch therefore concerns application-log settings, not the stored event records. Keep it distinct from the similarly named policy-tree branch and inspect the actual changed data before describing an access-policy change or an effect on log availability.

## Atomic claim

Application is the service-tree configuration branch for the Application event log.

Scope: **machine**

## Meaning in system-level logs

A Application registry event needs the exact entry and SDDL data when access configuration is involved; actual log-read or clear events are separate evidence.

### What the path cannot establish

- The path does not prove the Application log was read or cleared.
- The legacy access setting alone does not fully describe modern channel access.

### Applicability

The ADMX CSP lists supported Windows 10 builds with KB5005101 and Windows 11 21H2 onward on specified editions; it distinguishes legacy and modern access settings.


### Claim-level evidence

- **direct** — The legacy Application log-access policy maps to this service-tree branch.
  Section: Channel&#95;Log&#95;FileLogAccess&#95;5: ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog>)
- **direct** — The Application log receives events chosen by applications.
  Section: Standard logs table: Application.
  - [https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key](<https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **HAS_LEGACY_ACCESS_POLICY_COUNTERPART** (incoming): [Application](knowledge-d68f6f8882c9258690be94c9.md)
  Microsoft maps modern Application log access policy to the Software Policies location and its corresponding legacy access policy under Services EventLog. They are configuration locations for the same channel, not stores of the event records.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_1>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog>)
- [https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key](<https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;5](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_5>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
