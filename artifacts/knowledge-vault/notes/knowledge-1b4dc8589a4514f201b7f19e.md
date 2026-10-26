---
node_id: "knowledge:1b4dc8589a4514f201b7f19e"
generated: true
---

# Services

## Full prefix

~~~text
HKLM\System\CurrentControlSet\Services
~~~

- Domain: registry
- Depth: L4
- Node ID: `knowledge:1b4dc8589a4514f201b7f19e`

## Hierarchy

Parent: [CurrentControlSet](knowledge-47075c2ddad8552fd6d1728a.md)

Children:

- [&lt;ServiceName&gt;](knowledge-8a99ec31e70ed76edb8f16ac.md)
- [EventLog](knowledge-89e4e74b89345ca9e5655f84.md)
- [Tcpip6](knowledge-7a23ffc0cf3da054741fc9ab.md)

## Functional explanation

Status: **documented**

Role: service&#95;and&#95;driver&#95;configuration

Services organizes configuration for individual system services and drivers. Each service or driver has its own child key; values beneath that key can specify startup behavior and other component-specific parameters. A driver can also store its own configuration beneath a Parameters subkey. This parent node describes the namespace shared by those definitions, not the runtime state of any particular service.

## Atomic claim

Services organizes configuration entries for services and drivers.

Scope: **machine**

## Meaning in system-level logs

A Services event requires the concrete service child, setting, actor and operation result to identify a service configuration change.

### What the path cannot establish

- The parent does not establish a service start or stop.
- A configured service can be absent from runtime execution.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — Services contains per-service and per-driver configuration.
  Section: Introduction.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows](<https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows>)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;5](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_5>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;6](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_6>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;7](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_7>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;8](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_8>)
- [https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key](<https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key>)
- [https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
