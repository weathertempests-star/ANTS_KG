---
node_id: "knowledge:1c2208ee30eaf2de937e8b29"
generated: true
---

# Comdlg32

## Full prefix

~~~text
HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Comdlg32
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:1c2208ee30eaf2de937e8b29`

## Hierarchy

Parent: [Policies](knowledge-0c0778e8b36d2e9810ea000d.md)

Children:

- [Placesbar](knowledge-099545eb4e77d675ecf0b0df.md)

## Functional explanation

Status: **documented**

Role: common&#95;open&#95;dialog&#95;user&#95;policy

Comdlg32 is a user policy key for features of the standard common Open dialog. Microsoft maps policies for hiding its Back button, suppressing the recently used filename list, and removing the Places Bar to values here. These policies target the common-dialog implementation used by an application, rather than every file-selection interface. The documentation explicitly distinguishes applications using the Windows XP dialog style from the newer Windows Vista dialog style.

## Atomic claim

Stores user policies for controls in legacy-style common Open dialogs.

Scope: **user**

## Meaning in system-level logs

When this path appears in logs, identify the named value and the application/dialog implementation involved. A policy registry write alone does not show that an Open dialog was displayed or that a file was opened.

### What the path cannot establish

- The key alone does not specify which dialog control policy is configured.
- The documented legacy-style policies do not establish behavior for every modern or application-specific file picker.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply. The descriptions limit these controls to applications using the legacy Windows XP common-dialog style; Windows Vista introduced a different style to which they do not apply.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **NoBackButton** (value): Policy state for removing the Back button from the supported standard Open dialog.
- **NoFileMru** (value): Policy state for removing the recently used filename dropdown in the supported Open dialog.
- **NoPlacesBar** (value): Policy state for removing the shortcut bar from the supported Open dialog.

### Claim-level evidence

- **direct** — The three user policies share Comdlg32 and describe the Windows XP versus Windows Vista dialog-style limitation.
  Section: NoBackButton; NoFileMRU; NoPlacesBar / policy descriptions and ADMX mappings.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nobackbutton](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nobackbutton>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofilemru](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofilemru>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noplacesbar](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noplacesbar>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nobackbutton](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nobackbutton>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofilemru](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nofilemru>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noplacesbar](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#noplacesbar>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#placesbar](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#placesbar>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
