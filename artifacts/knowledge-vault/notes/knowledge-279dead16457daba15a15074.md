---
node_id: "knowledge:279dead16457daba15a15074"
generated: true
---

# Windows NT

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows NT
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:279dead16457daba15a15074`

## Hierarchy

Parent: [Microsoft](knowledge-e80dc586f12d3ed46b0f8a25.md)

Children:

- [CurrentVersion](knowledge-be5a4d3eb6874a0e96ffbe30.md)
- [DNSClient](knowledge-d147cfaf2958552b80b46fbf.md)
- [Printers](knowledge-3b4c71166c9c7fba64853b39.md)
- [Terminal Services](knowledge-2b49667c7ece4e1c60892843.md)

## Functional explanation

Status: **structural**

Role: windows&#95;nt&#95;policy&#95;namespace

This machine Windows NT policy namespace groups documented administrative branches for DNS Client, printers, Remote Desktop Services, and foreground Group Policy processing. Its grouping role is inferred from those child mappings. Windows NT is part of the registry namespace retained by modern Windows; the label alone does not date the system or indicate that every child feature is installed or available.

## Atomic claim

Groups machine policy branches for DNS, printing, Remote Desktop, and foreground Group Policy.

Scope: **machine**

## Meaning in system-level logs

Resolve the full descendant path before interpreting a target here. Registry operation, result, and setting data distinguish unrelated DNS, printer, session, and startup policies sharing this namespace.

### What the path cannot establish

- The prefix does not identify the Windows version or installed server role.
- It does not demonstrate DNS activity, printing, a Remote Desktop session, or Group Policy processing.

### Applicability

Structural namespace used across Windows releases; each descendant policy has independent edition, feature, and version support. The Windows NT label is not a version detector.


### Claim-level evidence

- **structural_inference** — DNS server policy maps beneath Windows NT&#92;DNSClient.
  Section: DNS&#95;NameServer.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;nameserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_nameserver>)
- **structural_inference** — Printer discovery limits map beneath Windows NT&#92;Printers&#92;Wizard.
  Section: DomainPrinters.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters>)
- **structural_inference** — Foreground Group Policy processing maps beneath Windows NT&#92;CurrentVersion&#92;Winlogon.
  Section: SyncForegroundPolicy.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;nameserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_nameserver>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;allowfqdnnetbiosqueries](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_allowfqdnnetbiosqueries>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;appendtomultilabelname](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_appendtomultilabelname>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;domain](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_domain>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;domainnamedevolutionlevel](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_domainnamedevolutionlevel>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;idnencoding](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_idnencoding>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;idnmapping](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_idnmapping>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;nameserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_nameserver>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;netbios](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_netbios>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;preferlocalresponsesoverlowerorderdns](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_preferlocalresponsesoverlowerorderdns>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;registeradaptername](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_registeradaptername>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;registerreverselookup](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_registerreverselookup>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;registrationenabled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_registrationenabled>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;registrationoverwritesinconflict](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_registrationoverwritesinconflict>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;registrationrefreshinterval](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_registrationrefreshinterval>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;registrationttl](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_registrationttl>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;searchlist](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_searchlist>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;smartmultihomednameresolution](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_smartmultihomednameresolution>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;smartprotocolreorder](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_smartprotocolreorder>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;updatesecuritylevel](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_updatesecuritylevel>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;updatetopleveldomainzones](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_updatetopleveldomainzones>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;usedomainnamedevolution](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_usedomainnamedevolution>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#turn&#95;off&#95;multicast](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#turn_off_multicast>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#syncforegroundpolicy>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#allowwebprinting](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#allowwebprinting>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#applicationdriverisolation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#applicationdriverisolation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#customizedsupporturl](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#customizedsupporturl>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#domainprinters>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#donotinstallcompatibledriverfromwindowsupdate](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#donotinstallcompatibledriverfromwindowsupdate>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#emfdespooling](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#emfdespooling>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#forcesoftwarerasterization](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#forcesoftwarerasterization>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#kmprintersareblocked](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#kmprintersareblocked>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#mxdwuselegacyoutputformatmsxps](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#mxdwuselegacyoutputformatmsxps>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nondomainprinters](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#nondomainprinters>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly&#95;win7](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly_win7>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist&#95;win7](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist_win7>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#physicallocation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#physicallocation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#physicallocationsupport](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#physicallocationsupport>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printdriverisolationexecutionpolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printdriverisolationexecutionpolicy>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printdriverisolationoverridecompat](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printdriverisolationoverridecompat>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printerserverthread](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printerserverthread>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#showjobtitleineventlogs](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#showjobtitleineventlogs>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#v4driverdisallowprinterextension](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#v4driverdisallowprinterextension>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;auto&#95;reconnect](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_auto_reconnect>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;camera&#95;redirection](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_camera_redirection>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;certificate&#95;template&#95;policy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_certificate_template_policy>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;allow&#95;signed&#95;files&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_allow_signed_files_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;allow&#95;unsigned&#95;files&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_allow_unsigned_files_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;audio](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_audio>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;audio&#95;capture](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_audio_capture>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;audio&#95;quality](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_audio_quality>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;clipboard](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_clipboard>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;com](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_com>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;default&#95;m](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_default_m>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;disable&#95;hardware&#95;mode](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_disable_hardware_mode>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;lpt](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_lpt>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;pnp](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_pnp>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;printer](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_printer>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;trusted&#95;certificate&#95;thumbprints&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_trusted_certificate_thumbprints_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;turn&#95;off&#95;udp](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_turn_off_udp>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;colordepth](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_colordepth>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;delete&#95;roaming&#95;user&#95;profiles](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_delete_roaming_user_profiles>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;disable&#95;remote&#95;desktop&#95;wallpaper](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_disable_remote_desktop_wallpaper>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;dx&#95;use&#95;full&#95;hwgpu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_dx_use_full_hwgpu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;easy&#95;print](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_easy_print>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;enablevirtualgraphics](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_enablevirtualgraphics>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;fallbackprintdrivertype](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_fallbackprintdrivertype>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;forcible&#95;logoff](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_forcible_logoff>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;join&#95;session&#95;directory](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_join_session_directory>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;keep&#95;alive](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_keep_alive>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;license&#95;secgroup](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_license_secgroup>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;license&#95;servers](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_license_servers>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;license&#95;tooltip](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_license_tooltip>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;max&#95;con&#95;policy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_max_con_policy>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;maxdisplayres](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_maxdisplayres>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;maxmonitor](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_maxmonitor>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;preventlicenseupgrade](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_preventlicenseupgrade>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;promt&#95;creds&#95;client&#95;comp](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_promt_creds_client_comp>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;rdsappx&#95;waitforregistration](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_rdsappx_waitforregistration>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;remotecontrol&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_remotecontrol_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;remotedesktopvirtualgraphics](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_remotedesktopvirtualgraphics>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;sd&#95;clustname](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_sd_clustname>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;sd&#95;expose&#95;address](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_sd_expose_address>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;sd&#95;loc](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_sd_loc>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;security&#95;layer&#95;policy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_security_layer_policy>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;select&#95;network&#95;detect](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_select_network_detect>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;select&#95;transport](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_select_transport>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;server&#95;advanced&#95;remotefx&#95;remoteapp](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_server_advanced_remotefx_remoteapp>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;server&#95;auth](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_server_auth>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;server&#95;avc444&#95;mode&#95;preferred](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_server_avc444_mode_preferred>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;server&#95;avc&#95;hw&#95;encode&#95;preferred](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_server_avc_hw_encode_preferred>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;server&#95;compressor](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_server_compressor>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;server&#95;image&#95;quality](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_server_image_quality>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;server&#95;legacy&#95;rfx](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_server_legacy_rfx>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;server&#95;profile](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_server_profile>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;server&#95;visexp](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_server_visexp>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;server&#95;wddm&#95;graphics&#95;driver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_server_wddm_graphics_driver>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;session&#95;end&#95;on&#95;limit&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_session_end_on_limit_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;sessions&#95;disconnected&#95;timeout&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_sessions_disconnected_timeout_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;sessions&#95;idle&#95;limit&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_sessions_idle_limit_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;sessions&#95;limits&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_sessions_limits_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;single&#95;session](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_single_session>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;smart&#95;card](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_smart_card>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;start&#95;program&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_start_program_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;temp&#95;delete](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_temp_delete>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;temp&#95;per&#95;session](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_temp_per_session>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;time&#95;zone](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_time_zone>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;tscc&#95;permissions&#95;policy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_tscc_permissions_policy>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;turnoff&#95;singleapp](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_turnoff_singleapp>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;uia](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_uia>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;usb&#95;redirection&#95;disable](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_usb_redirection_disable>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;user&#95;authentication&#95;policy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_user_authentication_policy>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;user&#95;home](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_user_home>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;user&#95;mandatory&#95;profiles](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_user_mandatory_profiles>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;user&#95;profiles](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_user_profiles>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
