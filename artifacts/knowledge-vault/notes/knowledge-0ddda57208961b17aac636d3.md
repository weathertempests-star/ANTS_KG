---
node_id: "knowledge:0ddda57208961b17aac636d3"
generated: true
---

# DeviceGuard

## Full prefix

~~~text
HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:0ddda57208961b17aac636d3`

## Hierarchy

Parent: [Windows](knowledge-448d4b3e7d83a6ebe3c51a2d.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: code&#95;integrity&#95;deployment&#95;policy

This machine DeviceGuard policy key contains the documented deployment control for a Code Integrity policy, used to determine which code may run on the computer. The reviewed ConfigCIPolicy setting maps to DeployConfigCIPolicy here. This specific deployment mechanism supports the single-policy format; the DeviceGuard key name alone does not describe every virtualization-based security feature or demonstrate that enforcement is active.

## Atomic claim

Stores the legacy Group Policy deployment control for a machine Code Integrity policy.

Scope: **machine**

## Meaning in system-level logs

A registry target here concerns the deployment setting. Inspect the value name, data, operation, and result, and use effective App Control policy or code-integrity events to determine whether a policy loaded and what it allowed or blocked.

### What the path cannot establish

- The path does not prove virtualization-based security or a code-integrity policy is running.
- A deployment setting does not establish that any executable was allowed, blocked, or executed.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. Microsoft states this Group Policy deployment supports single-policy format only and recommends alternative deployment methods for Windows 10 1903 and later or Windows 11.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **DeployConfigCIPolicy** (value): Controls the legacy Group Policy deployment of a Code Integrity policy.

### Claim-level evidence

- **direct** — ConfigCIPolicy deploys a Code Integrity policy and maps DeployConfigCIPolicy here; Group Policy deployment supports single-policy format only.
  Section: ConfigCIPolicy.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceguard#configcipolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceguard#configcipolicy>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceguard#configcipolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceguard#configcipolicy>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceguard#configcipolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceguard#configcipolicy>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
