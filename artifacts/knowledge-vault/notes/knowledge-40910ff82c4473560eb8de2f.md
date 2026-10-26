---
node_id: "knowledge:40910ff82c4473560eb8de2f"
generated: true
---

# RemovableStorageDevices

## Full prefix

~~~text
HKCU\Software\Policies\Microsoft\Windows\RemovableStorageDevices
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:40910ff82c4473560eb8de2f`

## Hierarchy

Parent: [Windows](knowledge-43021d03261165f313b86e60.md)

Children:

- [Custom](knowledge-351acb26602c3d693aa48361.md)

## Functional explanation

Status: **documented**

Role: user&#95;removable&#95;storage&#95;access&#95;policies

RemovableStorageDevices is the user policy location for documented removable-storage access restrictions and enforcement-related reboot settings. Deny&#95;All applies a broad deny policy across removable-storage classes, while child paths can address particular or custom classes. The key represents requested policy configuration rather than a list of currently attached devices. Microsoft also distinguishes a reboot policy’s enabled state from the configured wait time and notes that access-right changes may await restart.

## Atomic claim

Stores user removable-storage access policies and related reboot-enforcement configuration.

Scope: **user**

## Meaning in system-level logs

Inspect the relevant value or class-specific child, user SID, data, and policy-refresh/restart context. A registry event here cannot itself identify a storage device or prove that a read/write attempt was blocked.

### What the path cannot establish

- Parent-key presence does not prove Deny&#95;All is enabled or identify affected device classes.
- A configured access restriction may require restart and does not establish that an attempted operation was denied.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **Deny&#95;All** (value): Policy state for denying access to all removable-storage classes; the documented broad deny takes precedence over individual class settings.
- **RebootTimeinSeconds&#95;state** (value): Policy state for configuring a forced reboot wait; it is not itself the numeric duration.

### Claim-level evidence

- **direct** — The broad deny policy and reboot state map to this user key.
  Section: AccessRights&#95;RebootTime&#95;1; RemovableStorageClasses&#95;DenyAll&#95;Access&#95;1 / descriptions and ADMX mappings.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses&#95;denyall&#95;access&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses_denyall_access_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights&#95;reboottime&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights_reboottime_1>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights&#95;reboottime&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights_reboottime_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denyread&#95;access&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denyread_access_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denywrite&#95;access&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denywrite_access_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses&#95;denyall&#95;access&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses_denyall_access_1>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
