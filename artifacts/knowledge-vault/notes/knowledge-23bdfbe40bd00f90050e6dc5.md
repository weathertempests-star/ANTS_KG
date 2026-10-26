---
node_id: "knowledge:23bdfbe40bd00f90050e6dc5"
generated: true
---

# Explorer

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\Explorer
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:23bdfbe40bd00f90050e6dc5`

## Hierarchy

Parent: [Windows](knowledge-448d4b3e7d83a6ebe3c51a2d.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: explorer&#95;administrative&#95;policy

This machine Windows Explorer policy key hosts administrative settings for File Explorer and related shell features. Reviewed examples control remote shortcut icons, applying Mark of the Web to insecure-source copies, default libraries, and uninstall access from Start. These are component policies under Software Policies, distinct from the older CurrentVersion Policies Explorer branch. The exact setting determines whether the subject is presentation, file handling, or shell permissions.

## Atomic claim

Stores machine shell policies for File Explorer, libraries, shortcuts, and Start behavior.

Scope: **machine**

## Meaning in system-level logs

Inspect the exact value and data with the operation and result. A change to the shortcut-icon policy does not show a remote icon was loaded; a copy-tagging policy change does not demonstrate a particular file copy.

### What the path cannot establish

- The key does not establish folder browsing, a network connection, or a file operation.
- Start or shortcut policy does not demonstrate that an application was uninstalled or executed.

### Applicability

Machine shell policies have setting-specific Windows and shell-version support. The remote-shortcut and Start mappings use the documented Pro/Enterprise/Education/IoT ADMX CSP baseline; later file-tagging policies require checking their individual current applicability table.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **EnableShellShortcutIconRemotePath** (value): Controls whether shortcut icons may use remote paths.
- **DisableMotWOnInsecurePathCopy** (value): Controls suppressing Mark of the Web when copying files from insecure sources.
- **NoUninstallFromStart** (value): Controls removal of app uninstall access from Start.

### Claim-level evidence

- **direct** — The named value controls use of remote paths for shortcut icons.
  Section: EnableShellShortcutIconRemotePath.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enableshellshortcuticonremotepath](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enableshellshortcuticonremotepath>)
- **direct** — The named value controls suppression of Mark of the Web tags for files copied from insecure sources.
  Section: DisableMotWOnInsecurePathCopy.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablemotwoninsecurepathcopy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablemotwoninsecurepathcopy>)
- **direct** — NoUninstallFromStart removes the uninstall command from Start.
  Section: NoUninstallFromStart.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouninstallfromstart](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouninstallfromstart>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enableshellshortcuticonremotepath](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enableshellshortcuticonremotepath>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablemotwoninsecurepathcopy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablemotwoninsecurepathcopy>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouninstallfromstart](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouninstallfromstart>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouninstallfromstart](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouninstallfromstart>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#startpinappswheninstalled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#startpinappswheninstalled>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#checksamesourceandtargetforfranddfs](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#checksamesourceandtargetforfranddfs>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#defaultlibrarieslocation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#defaultlibrarieslocation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablemotwoninsecurepathcopy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablemotwoninsecurepathcopy>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enableshellshortcuticonremotepath](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enableshellshortcuticonremotepath>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#explorerribbonstartsminimized](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#explorerribbonstartsminimized>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nonewappalert](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nonewappalert>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#showhibernateoption](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#showhibernateoption>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#showsleepoption](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#showsleepoption>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
