---
node_id: "knowledge:8475e1dd7787d9b87b0adf46"
generated: true
---

# LanmanWorkstation

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows\LanmanWorkstation
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:8475e1dd7787d9b87b0adf46`

## Hierarchy

Parent: [Windows](knowledge-448d4b3e7d83a6ebe3c51a2d.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: smb&#95;client&#95;policy

This machine LanmanWorkstation policy key configures the SMB client used to access remote file shares. Documented policies control preferred cipher-suite order, handle caching for continuously available shares, and whether Offline Files can be used with those shares. These are client-side behaviors and differ from server-side LanmanServer policy. Their effects depend on remote share capabilities, server implementation, and the supported cipher set.

## Atomic claim

Stores machine SMB client policies for cipher preference and continuously available shares.

Scope: **machine**

## Meaning in system-level logs

Inspect the precise value and data with operation and result. A write to a caching policy does not establish that a file was opened or cached; an actual connection needs share, protocol, and negotiated-session evidence.

### What the path cannot establish

- The path does not identify a remote share or prove an SMB connection occurred.
- Policy permitting caching does not prove any file was cached, pinned, or available offline.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting. AES&#95;256 suites are unavailable on Windows 10 20H2 and earlier. Handle-caching policy has no effect on Windows Server Scale-out File Server shares; other server/cluster limitations are documented separately.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **EnableHandleCachingForCAFiles** (value): Controls permitting client handle caching on qualifying continuously available shares.
- **AllowOfflineFilesforCAShares** (value): Controls permitting Offline Files for continuously available shares.

### Claim-level evidence

- **direct** — This policy controls SMB client cipher suites and notes AES&#95;256 limitations on Windows 10 20H2 and earlier.
  Section: Pol&#95;CipherSuiteOrder.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol&#95;ciphersuiteorder](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol_ciphersuiteorder>)
- **direct** — EnableHandleCachingForCAFiles controls client handle caching on continuously available shares, with server-specific exclusions.
  Section: Pol&#95;EnableHandleCachingForCAFiles.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol&#95;enablehandlecachingforcafiles](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol_enablehandlecachingforcafiles>)
- **direct** — AllowOfflineFilesforCAShares controls Offline Files support on continuously available shares.
  Section: Pol&#95;EnableOfflineFilesforCAShares.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol&#95;enableofflinefilesforcashares](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol_enableofflinefilesforcashares>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **COMPLEMENTARY_SMB_ROLE** (incoming): [LanmanServer](knowledge-f15f5e49111333b937961136.md)
  LanmanServer policy controls the SMB server and LanmanWorkstation policy controls the SMB client, including distinct cipher-order preferences.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanserver#pol&#95;ciphersuiteorder](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanserver#pol_ciphersuiteorder>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol&#95;ciphersuiteorder](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol_ciphersuiteorder>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol&#95;ciphersuiteorder](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol_ciphersuiteorder>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol&#95;enablehandlecachingforcafiles](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol_enablehandlecachingforcafiles>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol&#95;enableofflinefilesforcashares](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol_enableofflinefilesforcashares>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol&#95;ciphersuiteorder](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol_ciphersuiteorder>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol&#95;enablehandlecachingforcafiles](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol_enablehandlecachingforcafiles>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol&#95;enableofflinefilesforcashares](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-lanmanworkstation#pol_enableofflinefilesforcashares>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
