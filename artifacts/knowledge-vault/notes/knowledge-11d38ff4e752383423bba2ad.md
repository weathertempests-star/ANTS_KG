---
node_id: "knowledge:11d38ff4e752383423bba2ad"
generated: true
---

# Workspaces

## Full prefix

~~~text
HKCU\SOFTWARE\Policies\Microsoft\Workspaces
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:11d38ff4e752383423bba2ad`

## Hierarchy

Parent: [Microsoft](knowledge-84a535c5fdfd000f10ca6203.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;remoteapp&#95;workspace&#95;connection&#95;policy

Workspaces is the documented user policy location for specifying the default RemoteApp and Desktop Connections feed URL. When the policy is enabled, the configured feed replaces the user’s existing default connection and the user cannot change it through the normal setting. The default connection also enables document associations with RemoteApp programs. The registry location describes connection configuration rather than confirming feed retrieval, resource installation, or a remote application launch.

## Atomic claim

Locates the user policy specifying the default RemoteApp and Desktop Connections feed URL.

Scope: **user**

## Meaning in system-level logs

Capture the configured URL data, account SID, writer, and policy state for logs here. Correlate feed-subscription and RemoteApp connection records before claiming the endpoint was contacted or an application ran.

### What the path cannot establish

- The policy path alone does not identify a configured feed URL.
- A feed URL setting does not prove successful retrieval, trusted-server status, credential use, or application execution.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply.


### Claim-level evidence

- **direct** — Microsoft maps default RemoteApp/Desktop connection URL policy to this key and explains replacement, user-change restrictions, and document associations.
  Section: TS&#95;RADC&#95;DefaultConnection / description and ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;radc&#95;defaultconnection](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_radc_defaultconnection>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;radc&#95;defaultconnection](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_radc_defaultconnection>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;radc&#95;defaultconnection](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_radc_defaultconnection>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
