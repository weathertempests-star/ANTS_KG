---
node_id: "knowledge:d461b8948f927bcda0cb61f5"
generated: true
---

# Classes

## Full prefix

~~~text
HKLM\SOFTWARE\Classes
~~~

- Domain: registry
- Depth: L3
- Node ID: `knowledge:d461b8948f927bcda0cb61f5`

## Hierarchy

Parent: [Software](knowledge-a84a70f48e5b3f471e5c2cc0.md)

Children:

- [&lt;FileExtension&gt;](knowledge-b875a05336091f5dc911d726.md)
- [&lt;ProgID&gt;](knowledge-53b893d3100e12c0aae8e38b.md)
- [AppID](knowledge-d75d46deb29de6b668c32577.md)
- [CLSID](knowledge-f389e1b5089624cbb0275d01.md)
- [Interface](knowledge-0693ca455af0f9286cfc6510.md)

## Functional explanation

Status: **documented**

Role: machine&#95;class&#95;registrations

Classes holds the machine contribution to file associations and COM registration. It supplies default registration data that can participate in the HKCR merged view. This explicit machine location is useful when distinguishing per-computer registration from user overrides. Interpret an observed registration together with the relevant extension, ProgID, class or interface identifier; this parent alone selects no executable and supplies no execution evidence.

## Atomic claim

Classes holds the machine contribution to file associations and COM registration.

Scope: **machine**

## Meaning in system-level logs

Class-registration events need the child identifier, value payload and process architecture to establish the changed registration.

### What the path cannot establish

- The machine entry may not be the effective user-view entry.
- Classes registration does not prove COM activation or file opening.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — HKLM Software Classes supplies machine default registrations.
  Section: Machine and user Classes branches.
  - [https://learn.microsoft.com/en-us/windows/win32/sysinfo/hkey-classes-root-key](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/hkey-classes-root-key>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **MERGES_MACHINE_REGISTRATION_FROM** (incoming): [HKCR](knowledge-8676a23f044533833c4be696.md)
  HKCR incorporates machine Classes registrations along with the applicable user Classes registrations.
  - [https://learn.microsoft.com/en-us/windows/win32/sysinfo/hkey-classes-root-key](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/hkey-classes-root-key>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/sysinfo/hkey-classes-root-key](<https://learn.microsoft.com/en-us/windows/win32/sysinfo/hkey-classes-root-key>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/win32/com/-file-extension--key](<https://learn.microsoft.com/en-us/windows/win32/com/-file-extension--key>)
- [https://learn.microsoft.com/en-us/windows/win32/com/-progid--key](<https://learn.microsoft.com/en-us/windows/win32/com/-progid--key>)
- [https://learn.microsoft.com/en-us/windows/win32/com/appid-key](<https://learn.microsoft.com/en-us/windows/win32/com/appid-key>)
- [https://learn.microsoft.com/en-us/windows/win32/com/clsid-key-hklm](<https://learn.microsoft.com/en-us/windows/win32/com/clsid-key-hklm>)
- [https://learn.microsoft.com/en-us/windows/win32/com/inprocserver32](<https://learn.microsoft.com/en-us/windows/win32/com/inprocserver32>)
- [https://learn.microsoft.com/en-us/windows/win32/com/interface-key](<https://learn.microsoft.com/en-us/windows/win32/com/interface-key>)
- [https://learn.microsoft.com/en-us/windows/win32/com/localserver32](<https://learn.microsoft.com/en-us/windows/win32/com/localserver32>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
