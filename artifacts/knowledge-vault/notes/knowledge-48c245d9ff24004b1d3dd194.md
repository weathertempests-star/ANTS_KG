---
node_id: "knowledge:48c245d9ff24004b1d3dd194"
generated: true
---

# AllUserInstallAgent

## Full prefix

~~~text
HKLM\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services\AllUserInstallAgent
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:48c245d9ff24004b1d3dd194`

## Hierarchy

Parent: [Terminal Services](knowledge-2b49667c7ece4e1c60892843.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: remote&#95;desktop&#95;app&#95;registration&#95;policy

This machine Terminal Services AllUserInstallAgent policy key stores LogonWaitForPackageRegistration, which controls waiting for application registration before presenting the Start screen to a new user. Microsoft documents a wait of up to six minutes when the policy is enabled, useful when customizing Start on Remote Desktop Session Host servers. The key configures registration timing rather than listing installed applications or proving package installation.

## Atomic claim

Controls delaying user sign-in while application registration completes.

Scope: **machine**

## Meaning in system-level logs

Inspect LogonWaitForPackageRegistration data with operation and result. To establish a sign-in delay or completed registration, correlate with the user session, package-registration records, timing, and outcome.

### What the path cannot establish

- The key does not identify a package or prove an application was installed.
- A configured wait does not show registration completed or that a user actually experienced a delay.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. The description emphasizes new-user application registration and RD Session Host Start customization; it is not a general installer-completion guarantee.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **LogonWaitForPackageRegistration** (value): Controls waiting for app registration before displaying Start at user sign-in.

### Claim-level evidence

- **direct** — The policy maps LogonWaitForPackageRegistration here and can suspend sign-in for up to six minutes to complete app registration.
  Section: TS&#95;RDSAppX&#95;WaitForRegistration.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;rdsappx&#95;waitforregistration](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_rdsappx_waitforregistration>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;rdsappx&#95;waitforregistration](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_rdsappx_waitforregistration>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;rdsappx&#95;waitforregistration](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_rdsappx_waitforregistration>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
