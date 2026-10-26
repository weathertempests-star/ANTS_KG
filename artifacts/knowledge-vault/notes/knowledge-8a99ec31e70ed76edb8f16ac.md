---
node_id: "knowledge:8a99ec31e70ed76edb8f16ac"
generated: true
---

# &lt;ServiceName&gt;

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Services\<ServiceName>
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:8a99ec31e70ed76edb8f16ac`

## Hierarchy

Parent: [Services](knowledge-1b4dc8589a4514f201b7f19e.md)

Children:

- [NetworkProvider](knowledge-25c987ad687d53225fd6004c.md)
- [Parameters](knowledge-9e9f09121b2ed725ef565381.md)
- [Performance](knowledge-f9dc477573ee0cec21fbb7f3.md)

## Functional explanation

Status: **documented**

Role: service&#95;configuration&#95;template

A service-name child is the configuration record for one service or driver. The placeholder expresses a registry schema, not a discovered service installation. Startup, service type and binary-related fields must be interpreted for the concrete component. Keep configuration changes separate from runtime control events: a stored start setting is different from a successful start request, a running process or a loaded kernel driver.

## Atomic claim

A service-name child is the configuration record for one service or driver.

Scope: **machine**

## Meaning in system-level logs

Preserve service name, exact setting, type/data and actor; correlate service-control or driver-load telemetry for runtime state.

### What the path cannot establish

- The placeholder does not prove a concrete service exists.
- Start configuration does not prove that the service has started.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **Start** (value): Configured startup category; interpretation depends on service or driver type.
- **ImagePath** (value): Registered binary location for a driver; for a Win32 service, the executable launch string can also contain arguments. Preserve the complete raw data and interpret it with the service type.

### Claim-level evidence

- **direct** — Each service or driver has its own child under Services.
  Section: Common Registry Keys and Values.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree>)
- **direct** — A Win32 service main function receives arguments from its registry ImagePath value.
  Section: Introduction.
  - [https://learn.microsoft.com/en-us/windows/win32/services/service-entry-point](<https://learn.microsoft.com/en-us/windows/win32/services/service-entry-point>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree>)
- [https://learn.microsoft.com/en-us/windows/win32/services/service-entry-point](<https://learn.microsoft.com/en-us/windows/win32/services/service-entry-point>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree>)
- [https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys>)

## Templates and candidate tags

- Placeholder component: true
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
