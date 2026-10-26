---
node_id: "knowledge:f7425a54e82fbb2abceaf8f1"
generated: true
---

# Network Connections

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\Network Connections
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:f7425a54e82fbb2abceaf8f1`

## Hierarchy

Parent: [Windows](knowledge-448d4b3e7d83a6ebe3c51a2d.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: network&#95;connections&#95;policy

This machine Network Connections policy key stores administrative controls associated with connection management and network presentation. The reviewed machine mappings include local-only status indication, Internet Connection Sharing UI, elevation when domain users set a network location, and a legacy Internet Connection Firewall control. These settings concern different Windows generations and are not a substitute for current firewall rule or network-session configuration.

## Atomic claim

Stores machine administrative policies for network connection UI and related controls.

Scope: **machine**

## Meaning in system-level logs

Use the exact value name, data, operation, and result to distinguish UI, location-setting privilege, or legacy firewall policy. Network connectivity and modern firewall enforcement require their own effective configuration and traffic evidence.

### What the path cannot establish

- The path does not establish a network connection or a firewall rule change.
- A legacy Internet Connection Firewall policy cannot establish current Windows firewall protection.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. The Internet Connection Firewall description is historical and explicitly discusses Windows XP Service Pack 2 replacement by Windows Firewall; do not generalize it to all modern firewall behavior.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **NC&#95;DoNotShowLocalOnlyIcon** (value): Controls hiding the local-access-only network status indication.
- **NC&#95;StdDomainUserSetLocation** (value): Controls whether domain users must elevate to set a network location.

### Claim-level evidence

- **direct** — The value controls presentation of the local-access-only network icon.
  Section: NC&#95;DoNotShowLocalOnlyIcon.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;donotshowlocalonlyicon](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_donotshowlocalonlyicon>)
- **direct** — This value controls whether domain users must elevate to set network location.
  Section: NC&#95;StdDomainUserSetLocation.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;stddomainusersetlocation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_stddomainusersetlocation>)
- **direct** — The documented policy concerns legacy Internet Connection Firewall and is superseded in the stated Windows Firewall scenario.
  Section: NC&#95;PersonalFirewallConfig.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;personalfirewallconfig](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_personalfirewallconfig>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;donotshowlocalonlyicon](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_donotshowlocalonlyicon>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;stddomainusersetlocation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_stddomainusersetlocation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;personalfirewallconfig](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_personalfirewallconfig>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;donotshowlocalonlyicon](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_donotshowlocalonlyicon>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;personalfirewallconfig](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_personalfirewallconfig>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;showsharedaccessui](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_showsharedaccessui>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;stddomainusersetlocation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_stddomainusersetlocation>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
