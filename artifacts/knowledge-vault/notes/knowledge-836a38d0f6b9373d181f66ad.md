---
node_id: "knowledge:836a38d0f6b9373d181f66ad"
generated: true
---

# Order

## Full prefix

~~~text
HKLM\SYSTEM\CurrentControlSet\Control\NetworkProvider\Order
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:836a38d0f6b9373d181f66ad`

## Hierarchy

Parent: [NetworkProvider](knowledge-c25d1e41d0885923e3abc8f3.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: network&#95;provider&#95;order

Order specifies the order in which network providers are considered. Its ProviderOrder value links provider names to the corresponding entries under the Services tree. This is an ordering configuration, not a history of attempted providers or a guarantee that every listed implementation is loadable. An analyst must retain the actual ordered data and resolve the service-specific registration before describing a particular provider selection.

## Atomic claim

Order specifies the order in which network providers are considered.

Scope: **machine**

## Meaning in system-level logs

Preserve the full ProviderOrder string and changed ordering; resolve names against service registrations and correlate actual provider activity separately.

### What the path cannot establish

- A listed provider need not have loaded successfully.
- The configuration does not show which provider handled a particular request.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **ProviderOrder** (value): Comma-separated provider key names in consideration order.

### Claim-level evidence

- **direct** — ProviderOrder is an ordered comma-separated list of provider names.
  Section: Order and ProviderOrder.
  - [https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **ORDERS_REGISTERED_PROVIDERS** (outgoing): [NetworkProvider](knowledge-25c987ad687d53225fd6004c.md)
  ProviderOrder names resolve to provider-specific registrations beneath Services.
  - [https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys](<https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-registry-keys>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
