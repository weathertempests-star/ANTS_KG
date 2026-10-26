---
node_id: "knowledge:0693ca455af0f9286cfc6510"
generated: true
---

# Interface

## Full prefix

~~~text
HKLM\SOFTWARE\Classes\Interface
~~~

- Domain: registry
- Depth: L4
- Node ID: `knowledge:0693ca455af0f9286cfc6510`

## Hierarchy

Parent: [Classes](knowledge-d461b8948f927bcda0cb61f5.md)

Children:

- [&lt;IID&gt;](knowledge-2537b36c5d4b38f8dabf849a.md)

## Functional explanation

Status: **structural**

Role: com&#95;interface&#95;registration&#95;namespace

Interface groups COM interface registrations by interface identifier. The parent separates interface metadata from COM class registrations. Its IID children describe interfaces, so an IID should not be treated as a class identifier or an executable path. Resolve the actual child and its documented entries before relating an observation to marshaling or another interface operation; the collection itself records no invocation history.

## Atomic claim

Interface groups COM interface registrations by interface identifier.

Scope: **machine**

## Meaning in system-level logs

An Interface event requires the IID child and changed entry to identify the affected interface registration.

### What the path cannot establish

- The parent does not identify an invoked method.
- An IID is not interchangeable with a CLSID.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **structural_inference** — Interface registrations have one IID subkey for each interface.
  Section: Registry Key and definition.
  - [https://learn.microsoft.com/en-us/windows/win32/com/interface-key](<https://learn.microsoft.com/en-us/windows/win32/com/interface-key>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/com/interface-key](<https://learn.microsoft.com/en-us/windows/win32/com/interface-key>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/win32/com/interface-key](<https://learn.microsoft.com/en-us/windows/win32/com/interface-key>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
