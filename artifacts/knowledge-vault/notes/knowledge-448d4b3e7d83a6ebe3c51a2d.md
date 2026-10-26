---
node_id: "knowledge:448d4b3e7d83a6ebe3c51a2d"
generated: true
---

# Windows

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:448d4b3e7d83a6ebe3c51a2d`

## Hierarchy

Parent: [Microsoft](knowledge-e80dc586f12d3ed46b0f8a25.md)

Children:

- [AppCompat](knowledge-22de066f0506ed65c7a267c7.md)
- [CurrentVersion](knowledge-4ae5e85830d0b0f0c277db29.md)
- [DeviceGuard](knowledge-0ddda57208961b17aac636d3.md)
- [DeviceInstall](knowledge-e7e8c5a04a32fbcd82807d8d.md)
- [DriverInstall](knowledge-02ff42145a16f3c7d42732eb.md)
- [EventLog](knowledge-8570aba32433b35a4a83423b.md)
- [Explorer](knowledge-23bdfbe40bd00f90050e6dc5.md)
- [Filesystems](knowledge-d4cadc393bdafdf292d38702.md)
- [LanmanServer](knowledge-f15f5e49111333b937961136.md)
- [LanmanWorkstation](knowledge-8475e1dd7787d9b87b0adf46.md)
- [Network Connections](knowledge-f7425a54e82fbb2abceaf8f1.md)
- [RemovableStorageDevices](knowledge-e14554bd0424fbeb5b50b563.md)
- [System](knowledge-5489fdffb503de87c7667245.md)
- [TCPIP](knowledge-35950a0f066a3ad7fbbffa69.md)
- [WinRM](knowledge-89f201b64adc5b339389bdd7.md)

## Functional explanation

Status: **structural**

Role: windows&#95;policy&#95;namespace

This machine Windows policy namespace groups component administrative settings, including installation restrictions, event-log policy, file-system controls, removable-storage access, and remote management. The grouping role is inferred from documented descendants rather than a standalone Windows-wide switch. It sits beside other Microsoft policy families, so similar names under Windows NT or CurrentVersion must retain their full registry context.

## Atomic claim

Groups machine administrative policy branches for Windows components.

Scope: **machine**

## Meaning in system-level logs

Continue to the full component path and value before interpreting a target here. Operation and result show the kind and outcome of registry access; value data identifies the setting being examined or modified.

### What the path cannot establish

- The Windows prefix alone does not identify a policy setting.
- It does not establish policy enablement, effective enforcement, or any component operation.

### Applicability

Structural namespace across multiple Windows components; descendant policies have independent edition, feature, and operating-system requirements.


### Claim-level evidence

- **structural_inference** — A device installation restriction maps under this Windows namespace.
  Section: DeviceInstall&#95;AllowAdminInstall.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;allowadmininstall](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_allowadmininstall>)
- **structural_inference** — A WinRM service authentication policy maps beneath the same namespace.
  Section: DisallowKerberos&#95;1.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_1>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;allowadmininstall](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_allowadmininstall>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_1>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatprevent16bitmach](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatprevent16bitmach>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatremoveprogramcompatproppage](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatremoveprogramcompatproppage>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffapplicationimpacttelemetry](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffapplicationimpacttelemetry>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffengine](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffengine>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprogramcompatibilityassistant_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprograminventory](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffprograminventory>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffswitchback](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffswitchback>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffuseractionrecord](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-appcompat#appcompatturnoffuseractionrecord>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#allowdomaindelaylock](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#allowdomaindelaylock>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#defaultcredentialprovider](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-credentialproviders#defaultcredentialprovider>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceguard#configcipolicy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceguard#configcipolicy>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;allowadmininstall](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_allowadmininstall>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;deniedpolicy&#95;detailtext](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_deniedpolicy_detailtext>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;deniedpolicy&#95;simpletext](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_deniedpolicy_simpletext>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;installtimeout](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_installtimeout>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;policy&#95;reboottime](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_policy_reboottime>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;removable&#95;deny](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_removable_deny>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall&#95;systemrestore](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#deviceinstall_systemrestore>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall&#95;classes&#95;allowuser](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-deviceinstallation#driverinstall_classes_allowuser>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;autobackup&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_autobackup_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;autobackup&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_autobackup_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;autobackup&#95;3](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_autobackup_3>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;autobackup&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_autobackup_4>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;3](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_3>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;filelogaccess&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_filelogaccess_4>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;retention&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_retention_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;retention&#95;3](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_retention_3>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;log&#95;retention&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_log_retention_4>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;logenabled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_logenabled>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;logfilepath&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_logfilepath_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;logfilepath&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_logfilepath_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;logfilepath&#95;3](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_logfilepath_3>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;logfilepath&#95;4](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_logfilepath_4>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel&#95;logmaxsize&#95;3](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-eventlog#channel_logmaxsize_3>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-filesys#symlinkevaluation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanserver#pol&#95;ciphersuiteorder](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanserver#pol_ciphersuiteorder>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanserver#pol&#95;hashpublication](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanserver#pol_hashpublication>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanserver#pol&#95;hashsupportversion](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanserver#pol_hashsupportversion>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanserver#pol&#95;honorciphersuiteorder](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanserver#pol_honorciphersuiteorder>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol&#95;ciphersuiteorder](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol_ciphersuiteorder>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol&#95;enablehandlecachingforcafiles](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol_enablehandlecachingforcafiles>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol&#95;enableofflinefilesforcashares](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol_enableofflinefilesforcashares>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#blockuserfromshowingaccountdetailsonsignin](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#blockuserfromshowingaccountdetailsonsignin>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableacrylicbackgroundonlogon](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#disableacrylicbackgroundonlogon>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#dontenumerateconnectedusers](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#dontenumerateconnectedusers>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#useoembackground](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-logon#useoembackground>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;donotshowlocalonlyicon](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_donotshowlocalonlyicon>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;forcetunneling](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_forcetunneling>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;personalfirewallconfig](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_personalfirewallconfig>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;showsharedaccessui](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_showsharedaccessui>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc&#95;stddomainusersetlocation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-networkconnections#nc_stddomainusersetlocation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights&#95;reboottime&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#accessrights_reboottime_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denyread&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denyread_access_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses&#95;denywrite&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#customclasses_denywrite_access_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removable&#95;remote&#95;allow&#95;access](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removable_remote_allow_access>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses&#95;denyall&#95;access&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-removablestorage#removablestorageclasses_denyall_access_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouninstallfromstart](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#nouninstallfromstart>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#startpinappswheninstalled](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-startmenu#startpinappswheninstalled>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#cleanupprofiles](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#cleanupprofiles>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#dontforceunloadhive](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#dontforceunloadhive>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#leaveappmgmtdata](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#leaveappmgmtdata>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#profileerroraction](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#profileerroraction>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#slowlinktimeout](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#slowlinktimeout>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#user&#95;home](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#user_home>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#userinfoaccessaction](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-userprofiles#userinfoaccessaction>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#checksamesourceandtargetforfranddfs](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#checksamesourceandtargetforfranddfs>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#defaultlibrarieslocation](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#defaultlibrarieslocation>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablemotwoninsecurepathcopy](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#disablemotwoninsecurepathcopy>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enableshellshortcuticonremotepath](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enableshellshortcuticonremotepath>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enablesmartscreen](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#enablesmartscreen>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#explorerribbonstartsminimized](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#explorerribbonstartsminimized>)
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
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nonewappalert](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#nonewappalert>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#showhibernateoption](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#showhibernateoption>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#showsleepoption](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsexplorer#showsleepoption>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;1](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_1>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos&#95;2](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-windowsremotemanagement#disallowkerberos_2>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-wininit#hiberboot](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-wininit#hiberboot>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
