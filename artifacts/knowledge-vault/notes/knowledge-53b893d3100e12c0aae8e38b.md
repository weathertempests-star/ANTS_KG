---
node_id: "knowledge:53b893d3100e12c0aae8e38b"
generated: true
---

# &lt;ProgID&gt;

## Full prefix

~~~text
HKLM\SOFTWARE\Classes\<ProgID>
~~~

- Domain: registry
- Depth: L4
- Node ID: `knowledge:53b893d3100e12c0aae8e38b`

## Hierarchy

Parent: [Classes](knowledge-d461b8948f927bcda0cb61f5.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: programmatic&#95;identifier&#95;template

A ProgID names a file-association or COM registration using a textual identifier. Shell registrations describe how an application handles a file type; COM-oriented registrations can associate the name with a CLSID. These uses must not be conflated: a file-association ProgID does not by itself establish a COM mapping. Resolve the actual child entries before assigning a class identity, handler command or application behavior.

## Atomic claim

A ProgID names a file-association or COM registration using a textual identifier.

Scope: **machine**

## Meaning in system-level logs

A ProgID event needs the concrete identifier and changed child or value to distinguish file-association behavior from a COM class mapping.

### What the path cannot establish

- A ProgID is not guaranteed globally unique.
- A file-association ProgID does not by itself establish a CLSID mapping or COM execution.

### Applicability

This describes the documented Windows registry namespace; available descendants and their behavior depend on the installed components and Windows release.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **CLSID** (subkey): Optional association to a COM class identifier in a COM-oriented ProgID registration.

### Claim-level evidence

- **direct** — A ProgID identifies a class and can map to a CLSID; uniqueness is not guaranteed.
  Section: Definition and Registry Entry.
  - [https://learn.microsoft.com/en-us/windows/win32/com/-progid--key](<https://learn.microsoft.com/en-us/windows/win32/com/-progid--key>)
- **direct** — The Shell uses ProgID entries to associate file types with applications and describe association behavior.
  Section: Introduction and Programmatic Identifier Elements Used by File Associations.
  - [https://learn.microsoft.com/en-us/windows/win32/shell/fa-progids](<https://learn.microsoft.com/en-us/windows/win32/shell/fa-progids>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **ASSOCIATES_EXTENSION_WITH** (incoming): [&lt;FileExtension&gt;](knowledge-b875a05336091f5dc911d726.md)
  An extension default value can name the ProgID represented by the ProgID schema.
  - [https://learn.microsoft.com/en-us/windows/win32/com/-file-extension--key](<https://learn.microsoft.com/en-us/windows/win32/com/-file-extension--key>)
- **MAPS_PROGRAMMATIC_NAME_TO_CLASS** (outgoing): [&lt;CLSID&gt;](knowledge-265a47625042ec0b6ff764f0.md)
  When present, a CLSID subkey in a COM-oriented ProgID registration maps that textual identifier to a class; this is not a requirement for every Shell file-association ProgID.
  - [https://learn.microsoft.com/en-us/windows/win32/com/-progid--key](<https://learn.microsoft.com/en-us/windows/win32/com/-progid--key>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/com/-progid--key](<https://learn.microsoft.com/en-us/windows/win32/com/-progid--key>)
- [https://learn.microsoft.com/en-us/windows/win32/shell/fa-progids](<https://learn.microsoft.com/en-us/windows/win32/shell/fa-progids>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/win32/com/-progid--key](<https://learn.microsoft.com/en-us/windows/win32/com/-progid--key>)

## Templates and candidate tags

- Placeholder component: true
- Template-dependent prefix: true

This prefix contains a placeholder or descends from one. Template matching is not implemented.

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
