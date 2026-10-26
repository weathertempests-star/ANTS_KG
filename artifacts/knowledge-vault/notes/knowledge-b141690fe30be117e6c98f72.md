---
node_id: "knowledge:b141690fe30be117e6c98f72"
generated: true
---

# InprocServer32

## Full prefix

~~~text
HKLM\SOFTWARE\Classes\CLSID\<CLSID>\InprocServer32
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:b141690fe30be117e6c98f72`

## Hierarchy

Parent: [&lt;CLSID&gt;](knowledge-265a47625042ec0b6ff764f0.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: com&#95;in&#95;process&#95;server&#95;template

InprocServer32 describes the in-process server registration for a COM class. Its unnamed value identifies the server path and ThreadingModel supplies apartment-related metadata. This fixed child remains dependent on a concrete parent CLSID. A registry write changes registration data; confirming a load requires separate module or activation evidence, including the process architecture and the effective registration view used by the client.

## Atomic claim

InprocServer32 describes the in-process server registration for a COM class.

Scope: **machine**

## Meaning in system-level logs

Record CLSID, unnamed or ThreadingModel value, data and registry view; correlate with module-load events only when investigating execution.

### What the path cannot establish

- A server path does not establish that its DLL exists or loaded.
- The suffix 32 alone is insufficient evidence of the accessing process architecture.

### Applicability

The cited COM registration contract discusses 32-bit compatibility and apartments; architecture must be resolved from the actual registry view and client.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **(unnamed value)** (value): Path to the in-process server.
- **ThreadingModel** (value): REG&#95;SZ apartment model such as Apartment, Both, Free or Neutral.

### Claim-level evidence

- **direct** — InprocServer32 contains a server path and ThreadingModel.
  Section: Registry Entry and Remarks.
  - [https://learn.microsoft.com/en-us/windows/win32/com/inprocserver32](<https://learn.microsoft.com/en-us/windows/win32/com/inprocserver32>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/com/inprocserver32](<https://learn.microsoft.com/en-us/windows/win32/com/inprocserver32>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/com/inprocserver32](<https://learn.microsoft.com/en-us/windows/win32/com/inprocserver32>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
