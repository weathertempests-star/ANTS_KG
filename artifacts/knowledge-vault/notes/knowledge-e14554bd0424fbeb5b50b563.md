---
node_id: "knowledge:e14554bd0424fbeb5b50b563"
generated: true
---

# RemovableStorageDevices

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\RemovableStorageDevices
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:e14554bd0424fbeb5b50b563`

## Hierarchy

Parent: [Windows](knowledge-448d4b3e7d83a6ebe3c51a2d.md)

Children:

- [Custom](knowledge-ffef3dcf7890dd3e0c2c20c6.md)

## Functional explanation

Status: **documented**

Role: removable&#95;storage&#95;access&#95;policy

This machine RemovableStorageDevices policy key controls access to removable-storage classes. Reviewed root settings can deny all such classes, permit direct device handles in remote sessions, or set reboot timing for enforcing changes. Custom descendants hold class-specific read and write policies. This is an access-control policy area, distinct from DeviceInstall policies that govern whether devices and their drivers can be installed.

## Atomic claim

Stores machine policy for removable-storage access, direct remote-session handles, and enforcement timing.

Scope: **machine**

## Meaning in system-level logs

Inspect the value, data, operation, and result; Deny&#95;All has different meaning from AllowRemoteDASD. A device read, write, connection, or denied request needs evidence identifying the device and operation outcome.

### What the path cannot establish

- The path does not demonstrate a removable device was connected or accessed.
- Configured denial does not prove a specific read or write was attempted or blocked.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **Deny&#95;All** (value): Controls denial of access to all removable-storage classes, taking precedence over individual class policies.
- **AllowRemoteDASD** (value): Controls permitting remote-session users to open direct removable-device handles.

### Claim-level evidence

- **direct** — Deny&#95;All prevents access to all removable storage classes and takes precedence over individual removable-storage policies.
  Section: RemovableStorageClasses&#95;DenyAll&#95;Access&#95;2.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses&#95;denyall&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses_denyall_access_2>)
- **direct** — AllowRemoteDASD permits normal remote-session users to open direct handles to removable storage devices.
  Section: Removable&#95;Remote&#95;Allow&#95;Access.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removable&#95;remote&#95;allow&#95;access](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removable_remote_allow_access>)
- **direct** — RebootTimeinSeconds&#95;state maps the enforcement-reboot timing policy here.
  Section: AccessRights&#95;RebootTime&#95;2.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights&#95;reboottime&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights_reboottime_2>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **COMPLEMENTARY_DEVICE_CONTROL** (incoming): [Restrictions](knowledge-f0c4d58f8c586c14ac4c7a0f.md)
  DeviceInstall restrictions control installation and driver updates, whereas RemovableStorageDevices policy controls access rights to storage classes; neither setting alone establishes the other operation was blocked.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;removable&#95;deny](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_removable_deny>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses&#95;denyall&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses_denyall_access_2>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses&#95;denyall&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses_denyall_access_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removable&#95;remote&#95;allow&#95;access](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removable_remote_allow_access>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights&#95;reboottime&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights_reboottime_2>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights&#95;reboottime&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights_reboottime_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denyread&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denyread_access_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denywrite&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denywrite_access_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removable&#95;remote&#95;allow&#95;access](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removable_remote_allow_access>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses&#95;denyall&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses_denyall_access_2>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
