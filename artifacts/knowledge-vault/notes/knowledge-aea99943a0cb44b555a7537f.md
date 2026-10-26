---
node_id: "knowledge:aea99943a0cb44b555a7537f"
generated: true
---

# Terminal Services

## Full prefix

~~~text
HKCU\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:aea99943a0cb44b555a7537f`

## Hierarchy

Parent: [Windows NT](knowledge-03bafa86f275d0c2b383c588.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: user&#95;remote&#95;desktop&#95;services&#95;policies

Terminal Services is a documented user policy key for Remote Desktop Services and connection-client controls. Representative settings determine whether validly signed RDP files and default RDP settings may start sessions, and whether Remote Desktop Connection may save passwords. Other policies at this same prefix govern session-related behavior, so it is a shared policy container. Client policy, host policy, and actual session activity must be distinguished when interpreting its contents.

## Atomic claim

Stores user Remote Desktop client and session-related policy configuration.

Scope: **user**

## Meaning in system-level logs

Inspect the exact value and whether it controls the client or a session-host behavior, together with applicable computer policy. A log at this prefix requires connection/session records to establish remote access or credential use.

### What the path cannot establish

- The key does not prove a remote session was initiated or authenticated.
- A password-saving policy state does not establish that credentials are stored or that a password was disclosed.

### Applicability

The cited user ADMX CSP mappings cover serviced Windows 10 baselines with KB5005101 and Windows 11 21H2 or later on the listed managed editions. Individual legacy-policy limitations still apply.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **AllowSignedFiles** (value): Policy state permitting or preventing validly signed RDP files and the user’s default RDP settings from starting connections.
- **DisablePasswordSaving** (value): When the associated policy is enabled, disables credential saving in Remote Desktop Connection.

### Claim-level evidence

- **direct** — Microsoft maps user policies for validly signed/default RDP settings and password saving to this key.
  Section: TS&#95;CLIENT&#95;ALLOW&#95;SIGNED&#95;FILES&#95;1; TS&#95;CLIENT&#95;DISABLE&#95;PASSWORD&#95;SAVING&#95;1 / descriptions and ADMX mappings.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **HAS_USER_POLICY_COUNTERPART** (incoming): [Terminal Services](knowledge-2b49667c7ece4e1c60892843.md)
  The idle-session time-limit policy has both machine and user forms; Microsoft states machine policy takes precedence when both are configured. This does not establish the state or precedence of every setting in these shared keys.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;sessions&#95;idle&#95;limit&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_sessions_idle_limit_2>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;allow&#95;signed&#95;files&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_allow_signed_files_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;disable&#95;password&#95;saving&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_disable_password_saving_1>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

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
