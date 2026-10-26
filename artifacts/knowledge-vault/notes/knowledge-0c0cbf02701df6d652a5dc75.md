---
node_id: "knowledge:0c0cbf02701df6d652a5dc75"
generated: true
---

# System

## Full prefix

~~~text
HKLM\System
~~~

- Domain: registry
- Depth: L2
- Node ID: `knowledge:0c0cbf02701df6d652a5dc75`

## Hierarchy

Parent: [HKLM](knowledge-23067446c79f6f808ec9de07.md)

Children:

- [CurrentControlSet](knowledge-47075c2ddad8552fd6d1728a.md)

## Functional explanation

Status: **documented**

Role: system&#95;configuration&#95;hive

The SYSTEM subtree holds operating-system configuration used for startup, device-driver loading, services, and other system behavior. It contains control-set configuration beneath the machine-wide root. At this layer, SYSTEM identifies the configuration area; individual service settings and startup parameters are represented by descendant keys and their values.

## Atomic claim

SYSTEM organizes operating-system startup and service configuration.

Scope: **machine**

## Meaning in system-level logs

A SYSTEM event needs the control-set branch, target key/value and operation result to identify the affected configuration.

### What the path cannot establish

- The hive does not identify which service changed.
- Its configuration does not establish the runtime state of a driver.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — System controls startup, drivers, services and operating-system behavior.
  Section: Remarks: System.
  - [https://learn.microsoft.com/en-us/dotnet/api/microsoft.win32.registry.localmachine](<https://learn.microsoft.com/en-us/dotnet/api/microsoft.win32.registry.localmachine>)

### Explanation sources

- [https://learn.microsoft.com/en-us/dotnet/api/microsoft.win32.registry.localmachine](<https://learn.microsoft.com/en-us/dotnet/api/microsoft.win32.registry.localmachine>)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

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
- [https://learn.microsoft.com/en-us/windows/win32/sysinfo/structure-of-the-registry](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/structure-of-the-registry>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
