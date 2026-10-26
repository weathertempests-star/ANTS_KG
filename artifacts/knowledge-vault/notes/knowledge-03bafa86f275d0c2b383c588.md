---
node_id: "knowledge:03bafa86f275d0c2b383c588"
generated: true
---

# Windows NT

## Full prefix

~~~text
HKCU\SOFTWARE\Policies\Microsoft\Windows NT
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:03bafa86f275d0c2b383c588`

## Hierarchy

Parent: [Microsoft](knowledge-84a535c5fdfd000f10ca6203.md)

Children:

- [Printers](knowledge-199b7b1f8ced6c8b25f2904c.md)
- [Terminal Services](knowledge-aea99943a0cb44b555a7537f.md)

## Functional explanation

Status: **structural**

Role: user&#95;windows&#95;nt&#95;policy&#95;namespace

This Windows NT branch groups documented printer and Remote Desktop Services policies within the current-user Microsoft policy tree. Its Printers descendants affect package Point and Print and printer discovery, while Terminal Services holds policies for remote-session clients and related settings. The historical product-family label does not identify the host operating-system generation. At this prefix, the role is structural grouping across components rather than one effective policy.

## Atomic claim

Groups user printer and Remote Desktop policy descendants under the Windows NT name.

Scope: **user**

## Meaning in system-level logs

Identify whether the suffix is Printers or Terminal Services before interpreting a registry event. The shared parent cannot establish either a print operation or a remote desktop connection.

### What the path cannot establish

- The parent prefix does not specify a child policy value or establish its enabled state.
- An access to this namespace does not prove the descendant feature was used or that a requested change succeeded.

### Applicability

Structural namespace inferred from the cited documented descendants. Each descendant has its own Windows version, feature, and policy-scope requirements.


### Claim-level evidence

- **structural_inference** — The printer package policy documents a descendant under this branch.
  Section: PackagePointAndPrintOnly / ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly>)
- **structural_inference** — The Remote Desktop client policy documents another descendant.
  Section: TS&#95;CLIENT&#95;ALLOW&#95;SIGNED&#95;FILES&#95;1 / ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;allow&#95;signed&#95;files&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_allow_signed_files_1>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;allow&#95;signed&#95;files&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_allow_signed_files_1>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#downlevelbrowse](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#downlevelbrowse>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#intranetprintersurl](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#intranetprintersurl>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printerdirectorysearchscope](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printerdirectorysearchscope>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;allow&#95;signed&#95;files&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_allow_signed_files_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;allow&#95;unsigned&#95;files&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_allow_unsigned_files_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;disable&#95;password&#95;saving&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_disable_password_saving_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;trusted&#95;certificate&#95;thumbprints&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_trusted_certificate_thumbprints_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;easy&#95;print&#95;user](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_easy_print_user>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;gateway&#95;policy&#95;auth&#95;method](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_gateway_policy_auth_method>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;gateway&#95;policy&#95;enable](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_gateway_policy_enable>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;gateway&#95;policy&#95;server](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_gateway_policy_server>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;remotecontrol&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_remotecontrol_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;session&#95;end&#95;on&#95;limit&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_session_end_on_limit_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;sessions&#95;disconnected&#95;timeout&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_sessions_disconnected_timeout_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;sessions&#95;idle&#95;limit&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_sessions_idle_limit_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;sessions&#95;limits&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_sessions_limits_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;start&#95;program&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_start_program_1>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
