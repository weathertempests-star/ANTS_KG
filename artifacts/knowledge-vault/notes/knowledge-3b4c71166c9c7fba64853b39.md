---
node_id: "knowledge:3b4c71166c9c7fba64853b39"
generated: true
---

# Printers

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows NT\Printers
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:3b4c71166c9c7fba64853b39`

## Hierarchy

Parent: [Windows NT](knowledge-279dead16457daba15a15074.md)

Children:

- [PackagePointAndPrint](knowledge-294cb40b081d15e04d353cb7.md)
- [Wizard](knowledge-7a1ee15945034fbaf8ca8e95.md)

## Functional explanation

Status: **documented**

Role: printing&#95;administrative&#95;policy

This machine Windows NT Printers policy key hosts printing administrative controls, including driver isolation, print rendering, Internet printing, and printer location behavior. PackagePointAndPrint and Wizard children hold separate package-connection and discovery policies. Settings span several Windows printing generations, so the exact value and supported feature matter. The policy key is separate from installed printer queues, queued print jobs, and the actual spool files.

## Atomic claim

Stores machine printing policy for drivers, rendering, discovery, and related service behavior.

Scope: **machine**

## Meaning in system-level logs

Inspect the exact value, data, operation, and result to identify the printing policy being accessed. A job submission, driver load, spooler crash, or printed output requires matching printing or process telemetry.

### What the path cannot establish

- The key does not identify an installed queue or demonstrate a print job occurred.
- Driver isolation policy does not prove a driver loaded or that a spooler failure was prevented.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. Application-driver isolation only affects applications opting in and requires relaunch after a change; spooler driver isolation is a separate policy. Legacy printing settings retain their feature-specific support limits.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **ApplicationDriverIsolation** (value): Controls isolation for qualifying application-loaded print drivers; it does not govern spooler-loaded drivers.
- **ForceCSREMFDespooling** (value): Controls print-job processing location for the documented Windows print-server scenario.

### Claim-level evidence

- **direct** — ApplicationDriverIsolation affects drivers loaded by applications that opt into isolation and is checked once per process.
  Section: ApplicationDriverIsolation.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#applicationdriverisolation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#applicationdriverisolation>)
- **direct** — This separate policy controls isolation for print drivers loaded by the spooler.
  Section: PrintDriverIsolationExecutionPolicy.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printdriverisolationexecutionpolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printdriverisolationexecutionpolicy>)
- **direct** — ForceCSREMFDespooling concerns client versus server processing for Windows print-server jobs.
  Section: EMFDespooling.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#emfdespooling](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#emfdespooling>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#applicationdriverisolation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#applicationdriverisolation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printdriverisolationexecutionpolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printdriverisolationexecutionpolicy>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#emfdespooling](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#emfdespooling>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#allowwebprinting](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#allowwebprinting>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#applicationdriverisolation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#applicationdriverisolation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#customizedsupporturl](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#customizedsupporturl>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#donotinstallcompatibledriverfromwindowsupdate](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#donotinstallcompatibledriverfromwindowsupdate>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#emfdespooling](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#emfdespooling>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#forcesoftwarerasterization](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#forcesoftwarerasterization>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#kmprintersareblocked](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#kmprintersareblocked>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#mxdwuselegacyoutputformatmsxps](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#mxdwuselegacyoutputformatmsxps>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nondomainprinters](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nondomainprinters>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly&#95;win7](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly_win7>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist&#95;win7](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist_win7>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#physicallocation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#physicallocation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#physicallocationsupport](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#physicallocationsupport>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printdriverisolationexecutionpolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printdriverisolationexecutionpolicy>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printdriverisolationoverridecompat](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printdriverisolationoverridecompat>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printerserverthread](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printerserverthread>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#showjobtitleineventlogs](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#showjobtitleineventlogs>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#v4driverdisallowprinterextension](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#v4driverdisallowprinterextension>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
