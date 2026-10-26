---
node_id: "knowledge:f0c4d58f8c586c14ac4c7a0f"
generated: true
---

# Restrictions

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\DeviceInstall\Restrictions
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:f0c4d58f8c586c14ac4c7a0f`

## Hierarchy

Parent: [DeviceInstall](knowledge-e7e8c5a04a32fbcd82807d8d.md)

Children:

- [DeniedPolicy](knowledge-c69468c30833d73adaeed64e.md)

## Functional explanation

Status: **documented**

Role: device&#95;installation&#95;restriction&#95;policy

This machine DeviceInstall Restrictions key stores policies limiting device installation and driver updates. Reviewed settings cover administrator override, denial of removable-device installation, and reboot timing used to enforce restriction changes. The DeniedPolicy child controls notification text rather than deciding permission. Restrictions on installing a device are distinct from denying read or write access to storage that is already installed.

## Atomic claim

Stores administrative restrictions and enforcement controls for machine device installation.

Scope: **machine**

## Meaning in system-level logs

Inspect the specific restriction value, data, operation, and result. A write to DenyRemovableDevices concerns installation policy; actual blocked installation requires the device identity and the installation outcome, while storage access is a separate operation.

### What the path cannot establish

- This key does not show a removable device was connected or denied access.
- Configured restrictions do not by themselves prove a particular installation was blocked or a reboot occurred.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **AllowAdminInstall** (value): Controls the administrator override for device installation restrictions.
- **DenyRemovableDevices** (value): Controls preventing removable-device installation and driver updates.
- **ForceReboot** (value): Controls forced reboot behavior for applying changed installation restrictions.

### Claim-level evidence

- **direct** — AllowAdminInstall controls administrator ability to install or update device drivers regardless of other restriction settings.
  Section: DeviceInstall&#95;AllowAdminInstall.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;allowadmininstall](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_allowadmininstall>)
- **direct** — DenyRemovableDevices prevents installing removable devices and updating existing removable-device drivers, subject to the documented policy precedence.
  Section: DeviceInstall&#95;Removable&#95;Deny.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;removable&#95;deny](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_removable_deny>)
- **direct** — ForceReboot controls reboot enforcement timing for device installation restriction changes.
  Section: DeviceInstall&#95;Policy&#95;RebootTime.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;policy&#95;reboottime](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_policy_reboottime>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **COMPLEMENTARY_DEVICE_CONTROL** (outgoing): [RemovableStorageDevices](knowledge-e14554bd0424fbeb5b50b563.md)
  DeviceInstall restrictions control installation and driver updates, whereas RemovableStorageDevices policy controls access rights to storage classes; neither setting alone establishes the other operation was blocked.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;removable&#95;deny](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_removable_deny>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses&#95;denyall&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses_denyall_access_2>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;allowadmininstall](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_allowadmininstall>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;removable&#95;deny](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_removable_deny>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;policy&#95;reboottime](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_policy_reboottime>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;allowadmininstall](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_allowadmininstall>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;deniedpolicy&#95;detailtext](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_deniedpolicy_detailtext>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;deniedpolicy&#95;simpletext](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_deniedpolicy_simpletext>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;policy&#95;reboottime](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_policy_reboottime>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;removable&#95;deny](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_removable_deny>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
