---
node_id: "knowledge:fee5bc5e4ba523ce4f2ebd39"
generated: true
---

# Netlogon

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Netlogon
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:fee5bc5e4ba523ce4f2ebd39`

## Hierarchy

Parent: [Microsoft](knowledge-e80dc586f12d3ed46b0f8a25.md)

Children:

- [Parameters](knowledge-c22f5e5cdc87969dd43ef30d.md)

## Functional explanation

Status: **structural**

Role: netlogon&#95;policy&#95;namespace

This machine Netlogon policy namespace groups administrative settings for finding domain controllers and related Active Directory domain behavior. The documented settings reside in its Parameters child and include DC Locator address selection, DNS registration, discovery retries, and compatibility controls. The parent role is inferred from these mappings; it is distinct from the Netlogon service configuration branch and from Netlogon diagnostic logs.

## Atomic claim

Groups machine policy parameters for Netlogon and domain-controller discovery.

Scope: **machine**

## Meaning in system-level logs

A target at this prefix indicates the Netlogon administrative policy area. Continue to Parameters and the value name; operation, result, and data distinguish inspection from a policy update.

### What the path cannot establish

- The path does not prove that the computer is a domain controller or even domain joined.
- It does not show a domain-controller lookup, DNS registration, or authentication occurred.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.


### Claim-level evidence

- **structural_inference** — DC Locator address type policy maps to the Parameters child.
  Section: Netlogon&#95;AddressTypeReturned.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;addresstypereturned](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_addresstypereturned>)
- **structural_inference** — Domain-controller site-specific DNS registration policy also maps to Parameters.
  Section: Netlogon&#95;AutoSiteCoverage.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;autositecoverage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_autositecoverage>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;addresstypereturned](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_addresstypereturned>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;autositecoverage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_autositecoverage>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#serveracceptscompound](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#serveracceptscompound>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;addresslookuponpingbehavior](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_addresslookuponpingbehavior>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;addresstypereturned](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_addresstypereturned>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;allowdnssuffixsearch](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_allowdnssuffixsearch>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;allownt4crypto](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_allownt4crypto>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;allowsinglelabeldnsdomain](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_allowsinglelabeldnsdomain>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;autositecoverage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_autositecoverage>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;avoidfallbacknetbiosdiscovery](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_avoidfallbacknetbiosdiscovery>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;avoidpdconwan](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_avoidpdconwan>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;backgroundretryinitialperiod](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_backgroundretryinitialperiod>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;backgroundretrymaximumperiod](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_backgroundretrymaximumperiod>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;backgroundretryquittime](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_backgroundretryquittime>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;backgroundsuccessfulrefreshperiod](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_backgroundsuccessfulrefreshperiod>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;debugflag](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_debugflag>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;dnsavoidregisterrecords](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_dnsavoidregisterrecords>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;dnsrefreshinterval](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_dnsrefreshinterval>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;dnssrvrecorduselowercasehostnames](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_dnssrvrecorduselowercasehostnames>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;dnsttl](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_dnsttl>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;expecteddialupdelay](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_expecteddialupdelay>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;forcerediscoveryinterval](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_forcerediscoveryinterval>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;gcsitecoverage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_gcsitecoverage>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;ignoreincomingmailslotmessages](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_ignoreincomingmailslotmessages>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;ldapsrvpriority](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_ldapsrvpriority>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;ldapsrvweight](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_ldapsrvweight>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;maximumlogfilesize](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_maximumlogfilesize>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;ndncsitecoverage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_ndncsitecoverage>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;negativecacheperiod](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_negativecacheperiod>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;netlogonsharecompatibilitymode](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_netlogonsharecompatibilitymode>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;nonbackgroundsuccessfulrefreshperiod](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_nonbackgroundsuccessfulrefreshperiod>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;pingurgencymode](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_pingurgencymode>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;scavengeinterval](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_scavengeinterval>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;sitecoverage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_sitecoverage>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;sitename](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_sitename>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;sysvolsharecompatibilitymode](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_sysvolsharecompatibilitymode>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;trynextclosestsite](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_trynextclosestsite>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;usedynamicdns](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_usedynamicdns>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
