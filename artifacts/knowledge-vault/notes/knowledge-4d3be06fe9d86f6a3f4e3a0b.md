---
node_id: "knowledge:4d3be06fe9d86f6a3f4e3a0b"
generated: true
---

# Network Connections

## Full prefix

~~~text
HKCU\Software\Policies\Microsoft\Windows\Network Connections
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:4d3be06fe9d86f6a3f4e3a0b`

## Hierarchy

Parent: [Windows](knowledge-43021d03261165f313b86e60.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;network&#95;connections&#95;administrative&#95;policies

Network Connections is a documented user policy key for controls on connection-management interfaces, including adding or removing network components and accessing advanced settings. These policies govern particular user actions and can depend on the user’s administrative status and a separate policy that extends legacy restrictions to administrators. They do not constitute the network adapter configuration or connection history. An exact setting and its documented prerequisites are necessary to explain effect.

## Atomic claim

Stores user policies governing supported Network Connections management actions.

Scope: **user**

## Meaning in system-level logs

Collect the specific NC&#95; value, account privileges, and related administrator-policy state in logs. A write here changes policy configuration; it does not itself identify a network connection attempt or adapter reconfiguration.

### What the path cannot establish

- This location alone does not establish a network endpoint, adapter state, or connection success.
- Some restrictions require NC&#95;EnableAdminProhibits to affect administrators, so a single value may not determine effective behavior.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **NC&#95;AddRemoveComponents** (value): Controls administrator access to adding/removing LAN or remote-access components, subject to the documented administrator-prohibitions prerequisite.
- **NC&#95;EnableAdminProhibits** (value): Controls whether the specified legacy Network Connections policies also restrict administrators.

### Claim-level evidence

- **direct** — Component-management restrictions and administrator applicability are documented under this user policy branch.
  Section: NC&#95;AddRemoveComponents; NC&#95;EnableAdminProhibits / descriptions and ADMX mappings.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;addremovecomponents](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_addremovecomponents>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;enableadminprohibits](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_enableadminprohibits>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;addremovecomponents](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_addremovecomponents>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;advancedsettings](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_advancedsettings>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;allowadvancedtcpipconfig](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_allowadvancedtcpipconfig>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;changebindstate](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_changebindstate>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;deletealluserconnection](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_deletealluserconnection>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;deleteconnection](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_deleteconnection>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;dialupprefs](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_dialupprefs>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;enableadminprohibits](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_enableadminprohibits>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;ipstatechecking](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_ipstatechecking>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;lanchangeproperties](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_lanchangeproperties>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;lanconnect](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_lanconnect>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;lanproperties](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_lanproperties>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;newconnectionwizard](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_newconnectionwizard>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;rasalluserproperties](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_rasalluserproperties>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;raschangeproperties](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_raschangeproperties>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;rasconnect](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_rasconnect>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;rasmyproperties](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_rasmyproperties>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;renamealluserrasconnection](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_renamealluserrasconnection>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;renameconnection](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_renameconnection>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;renamelanconnection](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_renamelanconnection>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;renamemyrasconnection](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_renamemyrasconnection>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;statistics](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_statistics>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
