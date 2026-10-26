---
node_id: "knowledge:4e101125ec54c0606e86ce0a"
generated: true
---

# Settings

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\DeviceInstall\Settings
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:4e101125ec54c0606e86ce0a`

## Hierarchy

Parent: [DeviceInstall](knowledge-e7e8c5a04a32fbcd82807d8d.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: device&#95;installation&#95;behavior&#95;policy

This machine DeviceInstall Settings key contains policy for how Windows carries out device installation activity, including installation task timeout and creation of restore points during qualifying driver activity. These operational settings differ from device allow or deny restrictions in the sibling Restrictions branch. Disabling normal restore-point creation here concerns driver-related activity and does not describe the entire System Restore configuration.

## Atomic claim

Stores device installation task timing and restore-point policy controls.

Scope: **machine**

## Meaning in system-level logs

Inspect the timeout parameter or DisableSystemRestore data with operation and result. The registry interaction does not show a task timed out or a restore point was created; those events need installation and restore evidence.

### What the path cannot establish

- The key does not establish that a driver installation occurred or timed out.
- DisableSystemRestore here does not by itself establish the state of every System Restore feature.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **DisableSystemRestore** (value): Controls suppressing restore points during device activity that would normally create them.

### Claim-level evidence

- **direct** — Device installation task timeout in seconds maps here.
  Section: DeviceInstall&#95;InstallTimeout.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;installtimeout](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_installtimeout>)
- **direct** — DisableSystemRestore controls preventing restore-point creation during device activity that normally prompts one.
  Section: DeviceInstall&#95;SystemRestore.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;systemrestore](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_systemrestore>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;installtimeout](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_installtimeout>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;systemrestore](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_systemrestore>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;installtimeout](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_installtimeout>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;systemrestore](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_systemrestore>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
