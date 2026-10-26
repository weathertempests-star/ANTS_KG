---
node_id: "knowledge:7a1ee15945034fbaf8ca8e95"
generated: true
---

# Wizard

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows NT\Printers\Wizard
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:7a1ee15945034fbaf8ca8e95`

## Hierarchy

Parent: [Printers](knowledge-3b4c71166c9c7fba64853b39.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: printer&#95;discovery&#95;policy

This machine Printers Wizard policy key stores administrative controls for the Add Printer discovery interface. The reviewed DomainPrinters and NonDomainPrinters policies set limits on displayed discovered printers depending on whether the computer can reach a domain controller. These are discovery and presentation settings rather than installed printer definitions. The descriptions contain version-specific limitations, including applying only TCP/IP printer limits in the stated scenario.

## Atomic claim

Configures Add Printer wizard display limits for managed and unmanaged network conditions.

Scope: **machine**

## Meaning in system-level logs

Inspect which policy state or limit parameter was accessed, with data, operation, and result. Actual discovery requires wizard or network evidence, and the policy name alone does not establish domain reachability at the event time.

### What the path cannot establish

- The key does not prove any printer was discovered, installed, or used.
- Domain/NonDomain policy names do not by themselves establish domain membership or current controller reachability.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. Microsoft distinguishes domain-controller reachability and explicitly narrows enabled behavior to TCP/IP limits, with separate Windows 10 default behavior. Do not apply historical wizard options indiscriminately to every modern printer UI.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **DomainDisplayPrinters&#95;State** (value): Enable state for Add Printer display limits under the documented managed-network condition.
- **NonDomainDisplayPrinters&#95;State** (value): Enable state for Add Printer display limits under the documented unmanaged-network condition.

### Claim-level evidence

- **direct** — DomainDisplayPrinters&#95;State maps the display-limit policy when a domain controller is reachable.
  Section: DomainPrinters.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters>)
- **direct** — NonDomainDisplayPrinters&#95;State maps the display-limit policy when a domain controller is not reachable; the text gives TCP/IP and Windows 10 limits.
  Section: NonDomainPrinters.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nondomainprinters](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nondomainprinters>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nondomainprinters](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nondomainprinters>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nondomainprinters](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nondomainprinters>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
