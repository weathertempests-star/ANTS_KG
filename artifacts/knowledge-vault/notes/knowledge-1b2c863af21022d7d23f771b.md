---
node_id: "knowledge:1b2c863af21022d7d23f771b"
generated: true
---

# System

## Full prefix

~~~text
HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:1b2c863af21022d7d23f771b`

## Hierarchy

Parent: [Policies](knowledge-0c0778e8b36d2e9810ea000d.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;system&#95;interface&#95;and&#95;profile&#95;policies

This System key holds documented user policies for several Windows system behaviors, including access to Registry Editor, replacement of the default Explorer user interface, and profile-size limits. It is a policy configuration location rather than the machine’s SYSTEM hive or a record of system-wide activity. Each setting has its own meaning, prerequisites, and Windows-version behavior, so interpretation must identify the exact policy and its data.

## Atomic claim

Stores user system policies for interface selection, administrative-tool access, and profile quotas.

Scope: **user**

## Meaning in system-level logs

Identify the policy value and account SID in logs under this key. For shell selection or profile limits, correlate the relevant sign-in/profile events; a registry operation alone does not show a replacement shell launched or a quota was exceeded.

### What the path cannot establish

- The key does not by itself prove Regedit is blocked or that a custom shell is selected.
- A configured profile limit does not establish current profile size or that logoff/synchronization was denied.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **EnableProfileQuota** (value): Policy state for limiting user-profile size; related options and Windows version determine the response.

### Claim-level evidence

- **direct** — Microsoft maps the user Registry Editor restriction to this System key.
  Section: DisableRegedit / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disableregedit](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disableregedit>)
- **direct** — The custom user-interface policy maps to this key and can replace Explorer at startup.
  Section: CustomShell / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#customshell](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#customshell>)
- **direct** — EnableProfileQuota is mapped here; profile-limit responses differ across Windows versions.
  Section: LimitSize / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#limitsize](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#limitsize>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disableregedit](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disableregedit>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#customshell](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#customshell>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#limitsize](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#limitsize>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disableregedit](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disableregedit>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#limitsize](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#limitsize>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#customshell](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#customshell>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#logonhoursnotificationpolicydescription](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#logonhoursnotificationpolicydescription>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#logonhourspolicydescription](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#logonhourspolicydescription>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#reportcachedlogonpolicydescription](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-winlogon#reportcachedlogonpolicydescription>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
