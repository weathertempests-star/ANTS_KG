---
node_id: "knowledge:e7e8c5a04a32fbcd82807d8d"
generated: true
---

# DeviceInstall

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\DeviceInstall
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:e7e8c5a04a32fbcd82807d8d`

## Hierarchy

Parent: [Windows](knowledge-448d4b3e7d83a6ebe3c51a2d.md)

Children:

- [Restrictions](knowledge-f0c4d58f8c586c14ac4c7a0f.md)
- [Settings](knowledge-4e101125ec54c0606e86ce0a.md)

## Functional explanation

Status: **structural**

Role: device&#95;installation&#95;policy&#95;namespace

This machine DeviceInstall policy namespace groups controls over device installation and driver updates associated with devices. Restrictions holds installation permission and enforcement controls, including custom denial notifications; Settings contains installation timeout and restore-point behavior. Its parent role is inferred from the documented child mappings. It is separate from DriverInstall, whose reviewed policy allows non-administrators to install driver packages for specified setup classes.

## Atomic claim

Groups machine restrictions and settings for device installation.

Scope: **machine**

## Meaning in system-level logs

Resolve Restrictions versus Settings and the actual value when interpreting a logged target. Operation, result, and data identify a registry interaction; device installation outcome requires installation telemetry for the relevant device.

### What the path cannot establish

- The key alone does not identify an attached device or driver package.
- It does not show installation was attempted, prevented, completed, or rolled back.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.


### Claim-level evidence

- **structural_inference** — Removable-device installation restrictions map to the Restrictions child.
  Section: DeviceInstall&#95;Removable&#95;Deny.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;removable&#95;deny](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_removable_deny>)
- **structural_inference** — Device installation task timeout maps to Settings.
  Section: DeviceInstall&#95;InstallTimeout.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;installtimeout](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_installtimeout>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **DISTINCT_INSTALLATION_POLICY_SCOPE** (outgoing): [DriverInstall](knowledge-02ff42145a16f3c7d42732eb.md)
  DeviceInstall groups device installation restrictions and operational settings; the reviewed DriverInstall restriction grants qualifying non-administrators driver-package installation for selected setup classes.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;removable&#95;deny](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_removable_deny>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall&#95;classes&#95;allowuser](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall_classes_allowuser>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;removable&#95;deny](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_removable_deny>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;installtimeout](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_installtimeout>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;allowadmininstall](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_allowadmininstall>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;deniedpolicy&#95;detailtext](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_deniedpolicy_detailtext>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;deniedpolicy&#95;simpletext](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_deniedpolicy_simpletext>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;installtimeout](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_installtimeout>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;policy&#95;reboottime](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_policy_reboottime>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;removable&#95;deny](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_removable_deny>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;systemrestore](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_systemrestore>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
