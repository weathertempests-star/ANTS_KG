---
node_id: "knowledge:2537b36c5d4b38f8dabf849a"
generated: true
---

# &lt;IID&gt;

## Full prefix

~~~text
HKLM\SOFTWARE\Classes\Interface\<IID>
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:2537b36c5d4b38f8dabf849a`

## Hierarchy

Parent: [Interface](knowledge-0693ca455af0f9286cfc6510.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: com&#95;interface&#95;configuration&#95;template

An IID child represents the registration of one COM interface. This template supplies an interface-identity slot within the machine registration tree. It is conceptually separate from the class implementing the interface and from any live object exposing it. A concrete registration and its child entries are needed to identify associated marshaling metadata; the placeholder alone does not establish installed code or interface use.

## Atomic claim

An IID child represents the registration of one COM interface.

Scope: **machine**

## Meaning in system-level logs

Retain the actual IID, child entry, operation and registry view when analyzing interface metadata changes.

### What the path cannot establish

- The template does not identify a concrete installed interface.
- Interface registration does not show that a method was called.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.


### Claim-level evidence

- **direct** — An IID subkey registers an interface identity.
  Section: Definition and Registry Key.
  - [https://learn.microsoft.com/en-us/windows/win32/com/interface-key](<https://learn.microsoft.com/en-us/windows/win32/com/interface-key>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/com/interface-key](<https://learn.microsoft.com/en-us/windows/win32/com/interface-key>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/com/interface-key](<https://learn.microsoft.com/en-us/windows/win32/com/interface-key>)

## Templates and candidate tags

- Placeholder component: true
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
