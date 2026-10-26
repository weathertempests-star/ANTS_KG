---
node_id: "knowledge:47075c2ddad8552fd6d1728a"
generated: true
---

# CurrentControlSet

## Full prefix

~~~text
HKLM\System\CurrentControlSet
~~~

- Domain: registry
- Depth: L3
- Node ID: `knowledge:47075c2ddad8552fd6d1728a`

## Hierarchy

Parent: [System](knowledge-0c0cbf02701df6d652a5dc75.md)

Children:

- [Control](knowledge-cf70125942441319173f4965.md)
- [Enum](knowledge-353bb9396036e898bd8afc17.md)
- [Hardware Profiles](knowledge-b2df5226b360738770b77f05.md)
- [Policies](knowledge-f73910e4222cd16401fa264d.md)
- [Services](knowledge-1b4dc8589a4514f201b7f19e.md)

## Functional explanation

Status: **documented**

Role: active&#95;system&#95;control&#95;set

CurrentControlSet exposes the currently active set of system configuration settings. Its descendants organize configuration relevant to system startup, device drivers, and system services: Control groups system-control settings, while Services contains configuration for individual services and drivers. This layer selects the active configuration context rather than a specific service or setting. The key path alone does not disclose the actual configuration values stored below it.

## Atomic claim

CurrentControlSet exposes the active system configuration context.

Scope: **machine**

## Meaning in system-level logs

CurrentControlSet records need the full child path and boot context; an offline numbered control-set path must not be treated as equivalent without evidence.

### What the path cannot establish

- The name alone does not identify the backing numbered control set.
- A configured service setting does not establish that the service is running.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — CurrentControlSet is the active control set used at runtime.
  Section: Cause of registry permission issues.
  - [https://learn.microsoft.com/en-us/troubleshoot/windows-client/shell-experience/uwp-apps-fails-incorrect-registry-permissions](<https://learn.microsoft.com/en-us/troubleshoot/windows-client/shell-experience/uwp-apps-fails-incorrect-registry-permissions>)
- **direct** — Control groups startup and device configuration in CurrentControlSet.
  Section: Introduction.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)
- **direct** — Services contains individual service and driver records.
  Section: Introduction.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree>)

### Explanation sources

- [https://learn.microsoft.com/en-us/troubleshoot/windows-client/shell-experience/uwp-apps-fails-incorrect-registry-permissions](<https://learn.microsoft.com/en-us/troubleshoot/windows-client/shell-experience/uwp-apps-fails-incorrect-registry-permissions>)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows](<https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows>)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-control-registry-tree>)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-enum-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-enum-registry-tree>)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;5](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_5>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;6](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_6>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;7](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_7>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;8](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_8>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#disablecompression](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#disablecompression>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#disabledeletenotification](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#disabledeletenotification>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#disableencryption](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#disableencryption>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#enablepagefileencryption](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#enablepagefileencryption>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#longpathsenabled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#longpathsenabled>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#shortnamecreationsettings](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#shortnamecreationsettings>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#txfdeprecatedfunctionality](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#txfdeprecatedfunctionality>)
- [https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexa](<https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexa>)
- [https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment](<https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-environment>)
- [https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key](<https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key>)
- [https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys>)
- [https://learn.microsoft.com/en-us/windows/win32/secauthn/registering-ssp-ap-dlls](<https://learn.microsoft.com/en-us/windows/win32/secauthn/registering-ssp-ap-dlls>)
- [https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
