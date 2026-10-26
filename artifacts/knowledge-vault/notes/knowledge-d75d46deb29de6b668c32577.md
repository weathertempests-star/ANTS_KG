---
node_id: "knowledge:d75d46deb29de6b668c32577"
generated: true
---

# AppID

## Full prefix

~~~text
HKLM\SOFTWARE\Classes\AppID
~~~

- Domain: registry
- Depth: L4
- Node ID: `knowledge:d75d46deb29de6b668c32577`

## Hierarchy

Parent: [Classes](knowledge-d461b8948f927bcda0cb61f5.md)

Children:

- [&lt;AppID&#95;GUID&gt;](knowledge-83629dfe2658e5b39e18f1fd.md)

## Functional explanation

Status: **structural**

Role: dcom&#95;application&#95;registration&#95;namespace

AppID groups application-level COM configuration registrations. Its GUID-named children can collect settings shared by multiple DCOM classes. The parent therefore represents a registration namespace rather than one executable or security policy. To interpret an observation, resolve the application identifier and the specific setting below it; do not copy a child application identity or launch rule onto the entire branch.

## Atomic claim

AppID groups application-level COM configuration registrations.

Scope: **machine**

## Meaning in system-level logs

An AppID namespace event needs the actual GUID child and value operation before identifying a DCOM configuration change.

### What the path cannot establish

- The parent does not designate one executable.
- Its existence does not prove remote activation is enabled.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **structural_inference** — AppID registrations centralize settings for DCOM objects.
  Section: Registry Key and definition.
  - [https://learn.microsoft.com/en-us/windows/win32/com/appid-key](<https://learn.microsoft.com/en-us/windows/win32/com/appid-key>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/com/appid-key](<https://learn.microsoft.com/en-us/windows/win32/com/appid-key>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/win32/com/appid-key](<https://learn.microsoft.com/en-us/windows/win32/com/appid-key>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
