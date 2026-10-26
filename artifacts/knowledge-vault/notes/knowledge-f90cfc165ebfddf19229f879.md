---
node_id: "knowledge:f90cfc165ebfddf19229f879"
generated: true
---

# Kerberos

## Full prefix

~~~text
HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System\Kerberos
~~~

- Domain: registry
- Depth: L8
- Node ID: `knowledge:f90cfc165ebfddf19229f879`

## Hierarchy

Parent: [System](knowledge-da597a2f1a374e635b122f88.md)

Children:

- [Parameters](knowledge-5fcf00f56f556eab12895737.md)

## Functional explanation

Status: **documented**

Role: kerberos&#95;policy&#95;configuration

This machine Kerberos policy key stores controls for mapping DNS host names to authentication realms, defining interoperable Kerberos V5 realms, and selecting KDC proxy servers. The Parameters child holds additional protocol switches. A realm is an authentication administrative domain, and a KDC issues Kerberos tickets; these policies influence how the Windows client finds or interacts with those services.

## Atomic claim

Groups machine Kerberos realm, proxy, and protocol policy settings.

Scope: **machine**

## Meaning in system-level logs

Inspect the particular enable marker or mapping entries, operation, result, and data. A policy read under Kerberos is not evidence that a ticket was requested or a proxy contacted; those conclusions need Kerberos or network telemetry.

### What the path cannot establish

- No realm, domain controller, or proxy can be identified from this parent path alone.
- The path does not establish ticket issuance, authentication success, or use of a mapping.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **domain&#95;realm&#95;Enabled** (value): Enable marker for the host-name-to-realm mapping policy.
- **KdcProxyServer&#95;Enabled** (value): Enable marker for domain-to-KDC-proxy policy mappings.

### Claim-level evidence

- **direct** — HostToRealm maps DNS host names and suffixes to realms and maps domain&#95;realm&#95;Enabled here.
  Section: HostToRealm.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#hosttorealm](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#hosttorealm>)
- **direct** — KdcProxyServer configures domain-suffix mappings to KDC proxy servers.
  Section: KdcProxyServer.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxyserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxyserver>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#hosttorealm](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#hosttorealm>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxyserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxyserver>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#alwayssendcompoundid](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#alwayssendcompoundid>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#devicepkinitenabled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#devicepkinitenabled>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#hosttorealm](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#hosttorealm>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxydisableserverrevocationcheck](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxydisableserverrevocationcheck>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxyserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxyserver>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#mitrealms](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#mitrealms>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#stricttarget](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#stricttarget>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
