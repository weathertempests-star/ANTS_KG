---
node_id: "knowledge:c22f5e5cdc87969dd43ef30d"
generated: true
---

# Parameters

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Netlogon\Parameters
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:c22f5e5cdc87969dd43ef30d`

## Hierarchy

Parent: [Netlogon](knowledge-fee5bc5e4ba523ce4f2ebd39.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: netlogon&#95;policy&#95;configuration

This machine Netlogon Parameters policy key holds controls for domain-controller discovery and related domain operations. Microsoft maps DC address type, site coverage, DNS suffix searching, registration, retry timing, and older cryptography compatibility policies here. Some settings affect clients and others apply to domain controllers. Values describe administrative choices for these functions rather than discovered domain controllers or records of domain authentication.

## Atomic claim

Stores machine Netlogon policies affecting domain-controller location, registration, and compatibility.

Scope: **machine**

## Meaning in system-level logs

Identify the value and machine role before interpreting a registry operation. A change to AutoSiteCoverage concerns domain-controller DNS registration policy; it does not establish a record was published, and a DC Locator setting does not report a lookup result.

### What the path cannot establish

- The key does not identify an actual selected domain controller or successful authentication.
- No claim about DNS publication or discovery failure follows without operational records and the relevant data.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. Individual settings apply to different domain-member or domain-controller roles; older cryptography options are compatibility controls and do not imply current protocol support.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **AddressTypeReturned** (value): Controls whether DC Locator returns IPv4/IPv6 addresses or IPv4-only results.
- **AutoSiteCoverage** (value): Controls automatic registration for the closest uncovered sites by domain controllers.
- **CompoundIdDisabled** (value): Controls configuration of the device Active Directory account for compound authentication; interpret policy options rather than assuming the name is a direct enabled flag.

### Claim-level evidence

- **direct** — AddressTypeReturned controls whether DC Locator can return IPv4 and IPv6 addresses.
  Section: Netlogon&#95;AddressTypeReturned.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;addresstypereturned](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_addresstypereturned>)
- **direct** — AutoSiteCoverage controls registration of site-specific DC Locator DNS records for otherwise uncovered sites.
  Section: Netlogon&#95;AutoSiteCoverage.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;autositecoverage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_autositecoverage>)
- **direct** — CompoundIdDisabled maps device Active Directory account compound-authentication policy here.
  Section: ServerAcceptsCompound.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#serveracceptscompound](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#serveracceptscompound>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;addresstypereturned](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_addresstypereturned>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon&#95;autositecoverage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-netlogon#netlogon_autositecoverage>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#serveracceptscompound](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#serveracceptscompound>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

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
