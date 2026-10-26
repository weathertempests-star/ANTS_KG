---
node_id: "knowledge:c69468c30833d73adaeed64e"
generated: true
---

# DeniedPolicy

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\DeviceInstall\Restrictions\DeniedPolicy
~~~

- Domain: registry
- Depth: L8
- Node ID: `knowledge:c69468c30833d73adaeed64e`

## Hierarchy

Parent: [Restrictions](knowledge-f0c4d58f8c586c14ac4c7a0f.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: device&#95;denial&#95;notification&#95;policy

This machine DeviceInstall Restrictions DeniedPolicy key stores presentation settings for notifications shown when device installation is blocked by policy. Microsoft maps separate custom notification-title and detail-text policies to this location. These settings explain a restriction to users; they do not select devices, impose an installation prohibition, or contain a historical list of denied installation attempts.

## Atomic claim

Stores custom notification text for device installations prevented by policy.

Scope: **machine**

## Meaning in system-level logs

A registry target here concerns denial-message configuration. Use the exact value, string data, operation, and result to interpret an edit; a separate device-installation record is needed to show a notification-triggering denial happened.

### What the path cannot establish

- The path is not evidence that an installation was denied.
- Custom message text does not identify the device restriction or the installation outcome.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.


### Claim-level evidence

- **direct** — This policy supplies custom detail text when policy prevents device installation.
  Section: DeviceInstall&#95;DeniedPolicy&#95;DetailText.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;deniedpolicy&#95;detailtext](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_deniedpolicy_detailtext>)
- **direct** — This policy supplies the custom notification title for a policy-blocked device installation.
  Section: DeviceInstall&#95;DeniedPolicy&#95;SimpleText.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;deniedpolicy&#95;simpletext](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_deniedpolicy_simpletext>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;deniedpolicy&#95;detailtext](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_deniedpolicy_detailtext>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;deniedpolicy&#95;simpletext](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_deniedpolicy_simpletext>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;deniedpolicy&#95;detailtext](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_deniedpolicy_detailtext>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;deniedpolicy&#95;simpletext](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_deniedpolicy_simpletext>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
