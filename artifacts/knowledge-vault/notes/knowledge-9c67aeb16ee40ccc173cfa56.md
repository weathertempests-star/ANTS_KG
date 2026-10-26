---
node_id: "knowledge:9c67aeb16ee40ccc173cfa56"
generated: true
---

# Restrictions

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\DriverInstall\Restrictions
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:9c67aeb16ee40ccc173cfa56`

## Hierarchy

Parent: [DriverInstall](knowledge-02ff42145a16f3c7d42732eb.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: driver&#95;installation&#95;privilege&#95;policy

This machine DriverInstall Restrictions key stores the policy permitting non-administrative members of Users to install driver packages for selected device setup classes. Microsoft maps AllowUserDeviceClasses here and requires qualifying driver signatures or trusted publishers. This is a class-based privilege exception for package installation; the name Restrictions should not be mistaken for the separate DeviceInstall restrictions that prevent installation of particular devices.

## Atomic claim

Stores setup-class policy for non-administrator driver package installation.

Scope: **machine**

## Meaning in system-level logs

Inspect AllowUserDeviceClasses and any associated class entries, operation, result, and data. To claim installation under this exception, additional records must identify the user, package, class GUID, signature status, and installation result.

### What the path cannot establish

- The path does not establish that all users can install arbitrary drivers.
- A policy read or write does not prove a driver was installed, loaded, or trusted.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **AllowUserDeviceClasses** (value): Enable control for the policy permitting non-administrator Users to install driver packages for specified setup classes.

### Claim-level evidence

- **direct** — AllowUserDeviceClasses maps here; the policy specifies setup-class GUIDs for non-administrator driver package installation with signing prerequisites.
  Section: DriverInstall&#95;Classes&#95;AllowUser.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall&#95;classes&#95;allowuser](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall_classes_allowuser>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall&#95;classes&#95;allowuser](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall_classes_allowuser>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall&#95;classes&#95;allowuser](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall_classes_allowuser>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
