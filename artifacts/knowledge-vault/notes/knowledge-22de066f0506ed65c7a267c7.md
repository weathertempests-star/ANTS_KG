---
node_id: "knowledge:22de066f0506ed65c7a267c7"
generated: true
---

# AppCompat

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\AppCompat
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:22de066f0506ed65c7a267c7`

## Hierarchy

Parent: [Windows](knowledge-448d4b3e7d83a6ebe3c51a2d.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: application&#95;compatibility&#95;policy

This machine AppCompat policy key controls Windows application compatibility features and associated collection or troubleshooting tools. Documented settings affect the compatibility engine, Program Compatibility Assistant, compatibility property page, application inventory, SwitchBack, Steps Recorder, and legacy 16-bit behavior. These are separate controls with different polarity and platform relevance; the key name does not identify an application, a compatibility fix, or an execution record.

## Atomic claim

Stores machine policies for application compatibility support, inventory, and related tools.

Scope: **machine**

## Meaning in system-level logs

Inspect the exact value, data, operation, and result. A DisablePCA write concerns compatibility-assistance policy, while a DisableInventory write concerns inventory collection; neither establishes that a program executed or data was transmitted.

### What the path cannot establish

- The path does not identify a program or prove a compatibility fix was applied.
- A configuration access does not establish application execution or inventory transmission.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. Legacy 16-bit controls depend on platform support, and collector behavior depends on the documented collection prerequisites; do not treat every historic feature as present on all current editions.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **DisableEngine** (value): Controls turning off the application compatibility engine.
- **DisablePCA** (value): Controls turning off the Program Compatibility Assistant.
- **DisableInventory** (value): Controls turning off the application inventory collector.

### Claim-level evidence

- **direct** — DisableEngine controls the application compatibility engine.
  Section: AppCompatTurnOffEngine.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffengine](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffengine>)
- **direct** — DisablePCA controls the Program Compatibility Assistant.
  Section: AppCompatTurnOffProgramCompatibilityAssistant&#95;2.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant_2>)
- **direct** — DisableInventory controls Inventory Collector and depends on the Customer Experience Improvement Program state.
  Section: AppCompatTurnOffProgramInventory.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprograminventory](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprograminventory>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffengine](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffengine>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprograminventory](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprograminventory>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatprevent16bitmach](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatprevent16bitmach>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatremoveprogramcompatproppage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatremoveprogramcompatproppage>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffapplicationimpacttelemetry](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffapplicationimpacttelemetry>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffengine](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffengine>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprograminventory](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprograminventory>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffswitchback](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffswitchback>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffuseractionrecord](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffuseractionrecord>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
