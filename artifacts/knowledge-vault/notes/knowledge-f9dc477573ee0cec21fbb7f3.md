---
node_id: "knowledge:f9dc477573ee0cec21fbb7f3"
generated: true
---

# Performance

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Services\<ServiceName>\Performance
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:f9dc477573ee0cec21fbb7f3`

## Hierarchy

Parent: [&lt;ServiceName&gt;](knowledge-8a99ec31e70ed76edb8f16ac.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: service&#95;performance&#95;registration&#95;template

Performance holds optional performance-monitoring registration for a service or driver. The documented driver convention describes a performance DLL and its exported entry points. This template identifies the registration area without asserting any particular counter set or provider binary. Counter collection and provider loading are runtime activities that require additional evidence beyond the existence or modification of this configuration key.

## Atomic claim

Performance holds optional performance-monitoring registration for a service or driver.

Scope: **machine**

## Meaning in system-level logs

A Performance event needs the concrete service, changed entry and DLL/function data; correlate performance collection separately.

### What the path cannot establish

- Registration does not prove counter collection occurred.
- The placeholder does not identify an actual performance DLL.

### Applicability

This describes the documented service/driver Performance convention, not every modern performance-counter provider model.


### Claim-level evidence

- **direct** — Performance describes optional monitoring DLL and exported functions.
  Section: Additional Keys: Performance.
  - [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree](<https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
