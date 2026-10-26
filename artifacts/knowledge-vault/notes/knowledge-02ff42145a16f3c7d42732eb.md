---
node_id: "knowledge:02ff42145a16f3c7d42732eb"
generated: true
---

# DriverInstall

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\DriverInstall
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:02ff42145a16f3c7d42732eb`

## Hierarchy

Parent: [Windows](knowledge-448d4b3e7d83a6ebe3c51a2d.md)

Children:

- [Restrictions](knowledge-9c67aeb16ee40ccc173cfa56.md)

## Functional explanation

Status: **structural**

Role: driver&#95;installation&#95;policy&#95;namespace

This machine DriverInstall policy namespace groups the Restrictions branch for administrative control of driver-package installation privileges. The reviewed descendant setting allows members of the built-in Users group to install driver packages for specified device setup classes, subject to signing requirements. This structural parent is separate from DeviceInstall, which groups device installation restrictions, notifications, timing, and restore-point behavior.

## Atomic claim

Groups policy allowing specified driver package classes to be installed by non-administrators.

Scope: **machine**

## Meaning in system-level logs

A target here locates the driver-installation policy family. Continue to Restrictions and the actual setting or class list, then inspect operation, result, and data before describing a privilege-policy change.

### What the path cannot establish

- The namespace does not identify a driver package or approved setup class.
- It does not establish that a non-administrator installed a driver or that driver code executed.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.


### Claim-level evidence

- **structural_inference** — The policy maps to DriverInstall&#92;Restrictions and permits specified setup-class driver packages for non-administrative Users subject to signing requirements.
  Section: DriverInstall&#95;Classes&#95;AllowUser.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall&#95;classes&#95;allowuser](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall_classes_allowuser>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **DISTINCT_INSTALLATION_POLICY_SCOPE** (incoming): [DeviceInstall](knowledge-e7e8c5a04a32fbcd82807d8d.md)
  DeviceInstall groups device installation restrictions and operational settings; the reviewed DriverInstall restriction grants qualifying non-administrators driver-package installation for selected setup classes.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;removable&#95;deny](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_removable_deny>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall&#95;classes&#95;allowuser](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall_classes_allowuser>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall&#95;classes&#95;allowuser](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall_classes_allowuser>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall&#95;classes&#95;allowuser](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall_classes_allowuser>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
