---
node_id: "knowledge:2c1db0fdec41e742e6756af4"
generated: true
---

# System

## Full prefix

~~~text
HKCU\Software\Policies\Microsoft\Windows\System
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:2c1db0fdec41e742e6756af4`

## Hierarchy

Parent: [Windows](knowledge-43021d03261165f313b86e60.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;command&#95;prompt&#95;access&#95;policy

This System key in Software&#92;Policies is the documented user policy location for preventing access to the interactive command prompt and controlling whether command batch files may run. The policy concerns Cmd.exe and .cmd/.bat processing according to its selected option. It differs from the System policy key under Microsoft&#92;Windows&#92;CurrentVersion&#92;Policies, which hosts other user system policies. The parent path alone does not specify the selected restriction.

## Atomic claim

Locates the user policy governing Cmd.exe access and batch-file processing.

Scope: **user**

## Meaning in system-level logs

For logs here, obtain the actual policy data and selected batch-processing option as well as the user SID. Process-creation or blocking records are needed to establish whether a particular command or script was attempted and what happened.

### What the path cannot establish

- The prefix does not prove Cmd.exe is blocked or determine the batch-processing option.
- This policy location does not establish controls on every shell, scripting host, or executable-launch mechanism.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply.


### Claim-level evidence

- **direct** — Microsoft maps the user command-prompt policy here and states that it also controls batch-file processing.
  Section: DisableCMD / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disablecmd](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disablecmd>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disablecmd](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disablecmd>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disablecmd](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disablecmd>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
