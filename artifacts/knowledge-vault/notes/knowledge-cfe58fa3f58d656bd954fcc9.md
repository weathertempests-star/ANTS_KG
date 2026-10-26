---
node_id: "knowledge:cfe58fa3f58d656bd954fcc9"
generated: true
---

# Audit

## Full prefix

~~~text
HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System\Audit
~~~

- Domain: registry
- Depth: L8
- Node ID: `knowledge:cfe58fa3f58d656bd954fcc9`

## Hierarchy

Parent: [System](knowledge-da597a2f1a374e635b122f88.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: audit&#95;policy&#95;configuration

This machine Audit policy key configures whether process command lines are included in process-creation security auditing. Microsoft maps ProcessCreationIncludeCmdLine&#95;Enabled here, and states that the setting applies only when Audit Process Creation is enabled. The resulting information belongs to Security event 4688. This registry key stores policy configuration rather than the event records, recorded commands, or a list of created processes.

## Atomic claim

Controls inclusion of command lines in process-creation audit events.

Scope: **machine**

## Meaning in system-level logs

A read or write targeting this key concerns audit configuration. Inspect ProcessCreationIncludeCmdLine&#95;Enabled data, operation, and result, then separately check effective process-creation auditing and the actual Security events before concluding command lines were recorded.

### What the path cannot establish

- The key does not establish that process-creation auditing is enabled or that event 4688 exists.
- A target here does not show that any process ran or reveal its command line.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **ProcessCreationIncludeCmdLine&#95;Enabled** (value): Controls command-line inclusion in process-creation audit records when the required audit policy is enabled.

### Claim-level evidence

- **direct** — The mapped value controls command-line inclusion in event 4688 and depends on Audit Process Creation being enabled.
  Section: IncludeCmdLine.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **AFFECTS_SAME_EVENT_CHANNEL** (outgoing): [Security](knowledge-f8703f687ac0bc949d59642e.md)
  The Audit command-line setting governs process-creation information emitted to the Security channel when required auditing is enabled; EventLog Security policy separately governs channel file management and access. Neither registry key stores the audit records.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_2>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings#includecmdline>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
