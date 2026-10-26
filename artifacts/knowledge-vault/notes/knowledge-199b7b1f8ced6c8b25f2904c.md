---
node_id: "knowledge:199b7b1f8ced6c8b25f2904c"
generated: true
---

# Printers

## Full prefix

~~~text
HKCU\Software\Policies\Microsoft\Windows NT\Printers
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:199b7b1f8ced6c8b25f2904c`

## Hierarchy

Parent: [Windows NT](knowledge-03bafa86f275d0c2b383c588.md)

Children:

- [PackagePointAndPrint](knowledge-20effaab1b56130d0f0a4f4c.md)
- [Wizard](knowledge-40cfe2a8f140c981c256d988.md)

## Functional explanation

Status: **structural**

Role: user&#95;printer&#95;policy&#95;namespace

Printers is the structural parent for documented user printer policies in this Windows NT policy branch. Its PackagePointAndPrint child governs package-aware printer connections, while Wizard contains settings for discovery through the Add Printer Wizard. The parent therefore locates policy configuration, rather than enumerating installed queues or recording print jobs. The particular child, value data, Windows version, and applicable policy precedence are needed to determine behavior.

## Atomic claim

Groups documented user policies for package printer connections and wizard discovery.

Scope: **user**

## Meaning in system-level logs

Use the suffix and values to distinguish package connection restrictions from wizard browsing options. A registry operation on this parent is not evidence that a printer driver was installed or that a document was printed.

### What the path cannot establish

- The parent prefix does not specify a child policy value or establish its enabled state.
- An access to this namespace does not prove the descendant feature was used or that a requested change succeeded.

### Applicability

Structural namespace inferred from the cited documented descendants. Each descendant has its own Windows version, feature, and policy-scope requirements.


### Claim-level evidence

- **structural_inference** — Separate PackagePointAndPrint and Wizard mappings establish the common printer-policy parent.
  Section: PackagePointAndPrintOnly; DownlevelBrowse / ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#downlevelbrowse](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#downlevelbrowse>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#intranetprintersurl](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#intranetprintersurl>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printerdirectorysearchscope](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printerdirectorysearchscope>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
