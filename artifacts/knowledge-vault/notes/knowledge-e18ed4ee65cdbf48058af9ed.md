---
node_id: "knowledge:e18ed4ee65cdbf48058af9ed"
generated: true
---

# Policies

## Full prefix

~~~text
HKCU\Software\Policies
~~~

- Domain: registry
- Depth: L3
- Node ID: `knowledge:e18ed4ee65cdbf48058af9ed`

## Hierarchy

Parent: [Software](knowledge-86ce335845d887ebaaec150e.md)

Children:

- [Microsoft](knowledge-84a535c5fdfd000f10ca6203.md)

## Functional explanation

Status: **structural**

Role: user&#95;software&#95;policy&#95;namespace

Software&#92;Policies is a structural namespace for policy-managed software configuration in the current-user hive. Microsoft documents user Group Policy certificate stores beneath its Microsoft child and numerous Windows administrative-template settings beneath Microsoft&#92;Windows. These children have separate meanings and consumers; the parent does not encode a global policy state. Its location identifies intended user policy scope but cannot by itself establish the management source or effective result.

## Atomic claim

Groups policy-related software configuration for the current user.

Scope: **user**

## Meaning in system-level logs

For a log under this branch, retain the account SID, full policy suffix, value data, and operation. The prefix alone cannot distinguish Group Policy, MDM, another management tool, or a direct registry write.

### What the path cannot establish

- The parent prefix does not specify a child policy value or establish its enabled state.
- An access to this namespace does not prove the descendant feature was used or that a requested change succeeded.

### Applicability

Structural namespace inferred from the cited documented descendants. Each descendant has its own Windows version, feature, and policy-scope requirements.


### Claim-level evidence

- **structural_inference** — The documented user Group Policy certificate store establishes this ancestor.
  Section: CERT&#95;SYSTEM&#95;CURRENT&#95;USER&#95;GROUP&#95;POLICY.
  - [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)
- **structural_inference** — The documented user Windows policy location establishes Windows administrative-policy ancestry.
  Section: AppCompatTurnOffProgramCompatibilityAssistant&#95;1 / ADMX mapping.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant_1>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant_1>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant_1>)
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
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#downlevelbrowse](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#downlevelbrowse>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#intranetprintersurl](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#intranetprintersurl>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintonly>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#packagepointandprintserverlist>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printerdirectorysearchscope](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-printing#printerdirectorysearchscope>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights&#95;reboottime&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights_reboottime_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denyread&#95;access&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denyread_access_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denywrite&#95;access&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denywrite_access_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses&#95;denyall&#95;access&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses_denyall_access_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disablecmd](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-shellcommandpromptregedittools#disablecmd>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#addsearchinternetlinkinstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#addsearchinternetlinkinstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#cleartilesonexit](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#cleartilesonexit>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#desktopappsfirstinappsview](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#desktopappsfirstinappsview>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#disableglobalsearchonappsview](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#disableglobalsearchonappsview>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#gotodesktoponsignin](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#gotodesktoponsignin>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearcheverywherelinkinstartmenu](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nosearcheverywherelinkinstartmenu>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenudownload](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenudownload>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenuhomegroup](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenuhomegroup>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenurecordedtv](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenurecordedtv>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenuvideos](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nostartmenuvideos>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouninstallfromstart](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouninstallfromstart>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#powerbuttonaction](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#powerbuttonaction>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showappsviewonstart](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showappsviewonstart>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showrunasdifferentuserinstart](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showrunasdifferentuserinstart>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showstartondisplaywithforegroundonwinkey](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#showstartondisplaywithforegroundonwinkey>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#startpinappswheninstalled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#startpinappswheninstalled>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;allow&#95;signed&#95;files&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_allow_signed_files_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;allow&#95;unsigned&#95;files&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_allow_unsigned_files_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;disable&#95;password&#95;saving&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_disable_password_saving_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;client&#95;trusted&#95;certificate&#95;thumbprints&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_client_trusted_certificate_thumbprints_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;easy&#95;print&#95;user](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_easy_print_user>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;gateway&#95;policy&#95;auth&#95;method](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_gateway_policy_auth_method>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;gateway&#95;policy&#95;enable](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_gateway_policy_enable>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;gateway&#95;policy&#95;server](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_gateway_policy_server>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;radc&#95;defaultconnection](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_radc_defaultconnection>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;remotecontrol&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_remotecontrol_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;session&#95;end&#95;on&#95;limit&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_session_end_on_limit_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;sessions&#95;disconnected&#95;timeout&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_sessions_disconnected_timeout_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;sessions&#95;idle&#95;limit&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_sessions_idle_limit_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;sessions&#95;limits&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_sessions_limits_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts&#95;start&#95;program&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-terminalserver#ts_start_program_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#defaultlibrarieslocation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#defaultlibrarieslocation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disableindexedlibraryexperience](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disableindexedlibraryexperience>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disableknownfolders](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disableknownfolders>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablesearchboxsuggestions](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablesearchboxsuggestions>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#explorerribbonstartsminimized](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#explorerribbonstartsminimized>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#hidecontentviewmodesnippets](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#hidecontentviewmodesnippets>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;internet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_internet>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;internetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_internetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;intranet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_intranet>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;intranetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_intranetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;localmachine](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_localmachine>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;localmachinelockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_localmachinelockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;restricted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_restricted>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;restrictedlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_restrictedlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;trusted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_trusted>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchpreview&#95;trustedlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchpreview_trustedlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;internet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_internet>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;internetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_internetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;intranet](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_intranet>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;intranetlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_intranetlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;localmachine](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_localmachine>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;localmachinelockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_localmachinelockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;restricted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_restricted>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;restrictedlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_restrictedlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;trusted](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_trusted>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz&#95;policy&#95;opensearchquery&#95;trustedlockdown](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#iz_policy_opensearchquery_trustedlockdown>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nosearchinternettryharderbutton](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nosearchinternettryharderbutton>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#tryharderpinnedlibrary](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#tryharderpinnedlibrary>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#tryharderpinnedopensearch](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#tryharderpinnedopensearch>)
- [https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations](<https://learn.microsoft.com/en-us/windows/win32/seccrypto/system-store-locations>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
