---
node_id: "knowledge:099545eb4e77d675ecf0b0df"
generated: true
---

# Placesbar

## Full prefix

~~~text
HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\comdlg32\Placesbar
~~~

- Domain: registry
- Depth: L8
- Node ID: `knowledge:099545eb4e77d675ecf0b0df`

## Hierarchy

Parent: [Comdlg32](knowledge-1c2208ee30eaf2de937e8b29.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: common&#95;dialog&#95;places&#95;bar&#95;item&#95;policy

Placesbar is the documented user policy location for configuring the items shown in the Places Bar of the Windows File/Open dialog. The policy can specify one to five shortcuts, including supported local or remote folders and common shell folders. It controls the displayed navigation choices, rather than recording files accessed by the user. Microsoft limits its documented application to programs using the Windows XP common-dialog style.

## Atomic claim

Configures the navigation items shown in the supported common-dialog Places Bar.

Scope: **user**

## Meaning in system-level logs

A registry event here concerns Places Bar configuration. Collect the configured item data, application identity, and dialog style before linking the setting to visible navigation choices.

### What the path cannot establish

- A configured shortcut is not evidence that its destination was visited or that a file was opened.
- The policy does not guarantee that a modern or custom file picker will display these entries.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply. The description explicitly excludes the newer Windows Vista dialog style and applies to programs using the Windows XP common-dialog style.


### Claim-level evidence

- **direct** — The user policy maps to this key and allows one through five displayed locations.
  Section: PlacesBar / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#placesbar](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#placesbar>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#placesbar](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#placesbar>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#placesbar](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#placesbar>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
