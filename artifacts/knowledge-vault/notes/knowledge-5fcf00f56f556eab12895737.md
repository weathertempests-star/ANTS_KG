---
node_id: "knowledge:5fcf00f56f556eab12895737"
generated: true
---

# Parameters

## Full prefix

~~~text
HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System\Kerberos\Parameters
~~~

- Domain: registry
- Depth: L9
- Node ID: `knowledge:5fcf00f56f556eab12895737`

## Hierarchy

Parent: [Kerberos](knowledge-f90cfc165ebfddf19229f879.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: kerberos&#95;protocol&#95;policy

This machine Kerberos Parameters key holds specific protocol policy switches rather than realm mapping lists. Documented settings cover compound authentication requests, certificate-based device authentication, certificate-revocation checks for KDC proxies, and acceptance of system-generated service principal names. These mechanisms have different prerequisites and meanings, so the Parameters name alone is insufficient to determine which authentication behavior is being configured.

## Atomic claim

Stores machine switches for Kerberos compound identity, device certificates, proxy revocation, and target handling.

Scope: **machine**

## Meaning in system-level logs

Identify the exact switch and its data from the registry record, including whether the access succeeded. A write to NoRevocationCheck concerns proxy certificate checking; it does not itself show a certificate was accepted or a Kerberos exchange occurred.

### What the path cannot establish

- The path alone does not determine the selected certificate-authentication mode.
- Configuration does not demonstrate compound authentication, certificate acceptance, or a successful ticket exchange.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **AlwaysSendCompoundId** (value): Controls sending compound authentication first when requested by the resource domain.
- **DevicePKInitEnabled** (value): Controls support and mode selection for device certificate authentication.
- **NoRevocationCheck** (value): Controls disabling revocation checks on the KDC proxy server certificate.

### Claim-level evidence

- **direct** — AlwaysSendCompoundId controls compound requests when the resource domain requests compound identity.
  Section: AlwaysSendCompoundId.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#alwayssendcompoundid](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#alwayssendcompoundid>)
- **direct** — Device certificate authentication has Automatic and Force options and requires a supporting domain controller.
  Section: DevicePKInitEnabled.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#devicepkinitenabled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#devicepkinitenabled>)
- **direct** — NoRevocationCheck controls revocation checking for the KDC proxy SSL certificate.
  Section: KdcProxyDisableServerRevocationCheck.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxydisableserverrevocationcheck](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxydisableserverrevocationcheck>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#alwayssendcompoundid](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#alwayssendcompoundid>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#devicepkinitenabled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#devicepkinitenabled>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxydisableserverrevocationcheck](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxydisableserverrevocationcheck>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#alwayssendcompoundid](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#alwayssendcompoundid>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#devicepkinitenabled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#devicepkinitenabled>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxydisableserverrevocationcheck](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#kdcproxydisableserverrevocationcheck>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#stricttarget](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-kerberos#stricttarget>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
