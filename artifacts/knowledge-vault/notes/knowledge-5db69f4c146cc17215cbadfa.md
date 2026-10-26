---
node_id: "knowledge:5db69f4c146cc17215cbadfa"
generated: true
---

# Client

## Full prefix

~~~text
HKLM\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services\Client
~~~

- Domain: registry
- Depth: L7
- Node ID: `knowledge:5db69f4c146cc17215cbadfa`

## Hierarchy

Parent: [Terminal Services](knowledge-2b49667c7ece4e1c60892843.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: remote&#95;desktop&#95;client&#95;policy

This machine Terminal Services Client policy key stores controls used by the Remote Desktop Connection client. Reviewed settings govern hardware-accelerated decoding, use of UDP in RDP connections, and redirection of supported RemoteFX USB devices. These concern client capabilities and choices rather than the local computer accepting incoming sessions. Hardware, client version, and supported redirection features determine which settings can affect a connection.

## Atomic claim

Stores machine policies for Remote Desktop client decoding, UDP transport, and supported USB redirection.

Scope: **machine**

## Meaning in system-level logs

Inspect the exact value or option, data, operation, and result. To identify actual transport, decoding, or USB redirection, require connection negotiation, client capability, and redirected-device evidence.

### What the path cannot establish

- The key does not establish that a Remote Desktop session exists or which transport was negotiated.
- Allowing supported USB redirection does not show a device was redirected or that every USB device is supported.
- The inverse wording of the hardware-disable policy must not be confused with the EnableHardwareMode value name.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. Hardware decoding requires supported hardware. USB policy explicitly covers supported RemoteFX USB devices, with version/feature prerequisites, and should not be generalized to every modern device-redirection mechanism.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **EnableHardwareMode** (value): Controls hardware decoding through the documented inverse disable policy; meaning requires the actual configured state.
- **fClientDisableUDP** (value): Controls disabling UDP so RDP uses only TCP.

### Claim-level evidence

- **direct** — EnableHardwareMode maps the policy preventing hardware-accelerated decoding; enabling that policy uses software decoding.
  Section: TS&#95;CLIENT&#95;DISABLE&#95;HARDWARE&#95;MODE.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;disable&#95;hardware&#95;mode](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_disable_hardware_mode>)
- **direct** — fClientDisableUDP maps the policy selecting TCP-only behavior rather than attempting both TCP and UDP.
  Section: TS&#95;CLIENT&#95;TURN&#95;OFF&#95;UDP.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;turn&#95;off&#95;udp](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_turn_off_udp>)
- **direct** — The policy permits redirection of other supported RemoteFX USB devices for selected user groups and maps to this Client key.
  Section: TS&#95;USB&#95;REDIRECTION&#95;DISABLE.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;usb&#95;redirection&#95;disable](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_usb_redirection_disable>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;disable&#95;hardware&#95;mode](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_disable_hardware_mode>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;turn&#95;off&#95;udp](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_turn_off_udp>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;usb&#95;redirection&#95;disable](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_usb_redirection_disable>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;disable&#95;hardware&#95;mode](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_disable_hardware_mode>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;turn&#95;off&#95;udp](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_turn_off_udp>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;usb&#95;redirection&#95;disable](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_usb_redirection_disable>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
