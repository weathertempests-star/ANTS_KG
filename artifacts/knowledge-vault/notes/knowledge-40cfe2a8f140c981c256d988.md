---
node_id: "knowledge:40cfe2a8f140c981c256d988"
generated: true
---

# Wizard

## Full prefix

~~~text
HKCU\Software\Policies\Microsoft\Windows NT\Printers\Wizard
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:40cfe2a8f140c981c256d988`

## Hierarchy

Parent: [Printers](knowledge-199b7b1f8ced6c8b25f2904c.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;printer&#95;wizard&#95;discovery&#95;policies

Wizard is the user policy key for documented printer-discovery settings used by the Add Printer Wizard, including whether it offers network browsing for shared printers. This is interface policy rather than a printer queue inventory. Microsoft states that removing the wizard’s network browse page does not prevent other programs from searching for shared printers or connecting to them, so the policy’s effect must remain scoped to the documented wizard behavior.

## Atomic claim

Stores user policies for printer discovery through the Add Printer Wizard.

Scope: **user**

## Meaning in system-level logs

Retain the exact value and data and identify the wizard/version in use. A policy write here does not show that a network browse occurred or that a printer was added.

### What the path cannot establish

- Disabling wizard browsing does not prohibit all printer discovery or network printing.
- The path alone identifies neither a printer nor a completed connection or installation.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **Downlevel Browse** (value): Policy state controlling whether the Add Printer Wizard displays its network shared-printer browsing page.

### Claim-level evidence

- **direct** — The user setting maps Downlevel Browse to this key and explicitly affects only the Add Printer Wizard.
  Section: DownlevelBrowse / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#downlevelbrowse](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#downlevelbrowse>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#downlevelbrowse](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#downlevelbrowse>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#downlevelbrowse](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#downlevelbrowse>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#intranetprintersurl](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#intranetprintersurl>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printerdirectorysearchscope](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printerdirectorysearchscope>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
