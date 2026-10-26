---
node_id: "knowledge:83629dfe2658e5b39e18f1fd"
generated: true
---

# &lt;AppID&#95;GUID&gt;

## Full prefix

~~~text
HKLM\SOFTWARE\Classes\AppID\<AppID_GUID>
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:83629dfe2658e5b39e18f1fd`

## Hierarchy

Parent: [AppID](knowledge-d75d46deb29de6b668c32577.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: dcom&#95;application&#95;configuration&#95;template

An AppID GUID child holds configuration shared by the COM classes associated with that application identity. The template names the application-level registration slot, while actual settings can describe security or hosting choices. Class-to-AppID association is separate from both the GUID name and runtime activation. A log interpretation needs the concrete identifier and changed value to distinguish an identity mapping from a permissions or hosting modification.

## Atomic claim

An AppID GUID child holds configuration shared by the COM classes associated with that application identity.

Scope: **machine**

## Meaning in system-level logs

Preserve the AppID GUID, value data and related CLSID mapping when interpreting a DCOM registration event.

### What the path cannot establish

- The placeholder does not identify an actual registered application.
- A configured hosting or permission value does not prove activation occurred.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **DllSurrogate** (value): Selects a surrogate host for DLL servers; empty data selects the system surrogate.
- **LaunchPermission** (value): Specifies principals permitted to start servers for the application.

### Claim-level evidence

- **direct** — AppID GUID registrations group common COM configuration.
  Section: Registry Key; Remarks.
  - [https://learn.microsoft.com/en-us/windows/win32/com/appid-key](<https://learn.microsoft.com/en-us/windows/win32/com/appid-key>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **ASSOCIATES_WITH_APPLICATION_CONFIGURATION** (incoming): [&lt;CLSID&gt;](knowledge-265a47625042ec0b6ff764f0.md)
  A concrete class can associate with an AppID registration through its AppID metadata.
  - [https://learn.microsoft.com/en-us/windows/win32/com/appid-key](<https://learn.microsoft.com/en-us/windows/win32/com/appid-key>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/com/appid-key](<https://learn.microsoft.com/en-us/windows/win32/com/appid-key>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/com/appid-key](<https://learn.microsoft.com/en-us/windows/win32/com/appid-key>)

## Templates and candidate tags

- Placeholder component: true
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
