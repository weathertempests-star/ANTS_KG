---
node_id: "knowledge:89f201b64adc5b339389bdd7"
generated: true
---

# WinRM

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\WinRM
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:89f201b64adc5b339389bdd7`

## Hierarchy

Parent: [Windows](knowledge-448d4b3e7d83a6ebe3c51a2d.md)

Children:

- [Client](knowledge-d2343a9ac128221d53510a12.md)
- [Service](knowledge-1c488ca7b6bc263a06dc1a5d.md)

## Functional explanation

Status: **structural**

Role: winrm&#95;policy&#95;namespace

This machine WinRM policy namespace groups administrative controls for Windows Remote Management, with Client and Service descendants separating outgoing client behavior from incoming service behavior. The reviewed settings regulate Kerberos authentication in those two roles. The namespace role is inferred from the descendant mappings; it is distinct from service installation, listener configuration, connection records, and the remote tasks that WinRM can carry.

## Atomic claim

Separates machine policies for WinRM client and service authentication behavior.

Scope: **machine**

## Meaning in system-level logs

Resolve Client versus Service before interpreting the same AllowKerberos value name. Operation, status, and data identify the registry interaction; a WinRM session needs separate listener, authentication, or network evidence.

### What the path cannot establish

- The parent does not establish that WinRM is running or listening.
- It does not prove a remote connection, authentication, command, or successful task occurred.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.


### Claim-level evidence

- **structural_inference** — WinRM client Kerberos policy maps to Client.
  Section: DisallowKerberos&#95;2.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_2>)
- **structural_inference** — WinRM service Kerberos credential-acceptance policy maps to Service.
  Section: DisallowKerberos&#95;1.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_1>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_1>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_2>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
