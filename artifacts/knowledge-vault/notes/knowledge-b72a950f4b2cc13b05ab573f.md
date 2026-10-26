---
node_id: "knowledge:b72a950f4b2cc13b05ab573f"
generated: true
---

# AppCompat

## Full prefix

~~~text
HKCU\Software\Policies\Microsoft\Windows\AppCompat
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:b72a950f4b2cc13b05ab573f`

## Hierarchy

Parent: [Windows](knowledge-43021d03261165f313b86e60.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;compatibility&#95;assistant&#95;legacy&#95;policy

This AppCompat key is the documented user location for the legacy DisablePCA policy associated with Program Compatibility Assistant. Microsoft explicitly states that the user setting exists only for backward compatibility and is not valid for the documented Windows version, directing administrators to the computer-configuration setting instead. Accordingly, the path can identify historical or retained policy configuration without demonstrating that Program Compatibility Assistant is currently disabled.

## Atomic claim

Holds the backward-compatibility-only user Program Compatibility Assistant policy mapping.

Scope: **user**

## Meaning in system-level logs

A log showing DisablePCA here should be interpreted as access to a legacy user policy location. Obtain OS version and effective computer policy before concluding that compatibility assistance changed.

### What the path cannot establish

- DisablePCA under this HKCU path does not establish that Program Compatibility Assistant is disabled on current Windows.
- The path does not show that an application compatibility problem occurred or that a compatibility fix ran.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply. Crucial exception: the user Program Compatibility Assistant setting is explicitly backward-compatibility-only and not valid for the Windows version documented; use the computer policy to assess current behavior.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **DisablePCA** (value): Legacy user policy mapping for turning off Program Compatibility Assistant; the cited current documentation says this user setting is not valid and points to Computer Configuration.

### Claim-level evidence

- **direct** — Microsoft maps user DisablePCA here but explicitly labels the setting backward-compatibility-only and invalid for this Windows version.
  Section: AppCompatTurnOffProgramCompatibilityAssistant&#95;1 / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant_1>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant_1>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant_1>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
