---
node_id: "knowledge:ffef3dcf7890dd3e0c2c20c6"
generated: true
---

# Custom

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\RemovableStorageDevices\Custom
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:ffef3dcf7890dd3e0c2c20c6`

## Hierarchy

Parent: [RemovableStorageDevices](knowledge-e14554bd0424fbeb5b50b563.md)

Children:

- [Deny&#95;Read](knowledge-b71b05661651cc83f6f68012.md)
- [Deny&#95;Write](knowledge-75a48b044d3aa7c585926697.md)

## Functional explanation

Status: **structural**

Role: custom&#95;removable&#95;storage&#95;policy&#95;namespace

This machine RemovableStorageDevices Custom namespace groups policies for removable-storage classes selected by an administrator rather than a predefined class branch. Its Deny&#95;Read and Deny&#95;Write children separate read restrictions from write restrictions. This grouping role is inferred from documented mappings to those children. The Custom parent is not itself a denial flag, a device identifier, or evidence of access to a physical drive.

## Atomic claim

Groups separate machine read and write policies for custom removable-storage classes.

Scope: **machine**

## Meaning in system-level logs

Continue to the read or write policy child and inspect enable data and class entries with operation and result. The Custom parent alone cannot identify an affected device class or access right.

### What the path cannot establish

- The parent does not indicate whether reads, writes, both, or neither are denied.
- It does not identify the selected classes or show that any device access took place.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.


### Claim-level evidence

- **structural_inference** — The custom-class read-access policy maps to Custom&#92;Deny&#95;Read.
  Section: CustomClasses&#95;DenyRead&#95;Access&#95;2.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denyread&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denyread_access_2>)
- **structural_inference** — The custom-class write-access policy maps to Custom&#92;Deny&#95;Write.
  Section: CustomClasses&#95;DenyWrite&#95;Access&#95;2.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denywrite&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denywrite_access_2>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denyread&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denyread_access_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denywrite&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denywrite_access_2>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denyread&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denyread_access_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denywrite&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denywrite_access_2>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
