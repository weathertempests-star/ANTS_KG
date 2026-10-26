---
node_id: "knowledge:bce036ca2ffd77b92b30b75c"
generated: true
---

# Windows Defender

## Full prefix

~~~text
HKLM\SOFTWARE\Policies\Microsoft\Windows Defender
~~~

- Domain: registry
- Depth: L5
- Node ID: `knowledge:bce036ca2ffd77b92b30b75c`

## Hierarchy

Parent: [Microsoft](knowledge-e80dc586f12d3ed46b0f8a25.md)

Children:

- [MpEngine](knowledge-f5f0202ed1957d374c51497d.md)

## Functional explanation

Status: **structural**

Role: defender&#95;policy&#95;namespace

This machine Windows Defender policy namespace groups Microsoft Defender Antivirus administrative settings. In this inventory, the supported descendant evidence is the MpEngine branch used to select cloud protection aggressiveness. The parent grouping role is inferred from that documented location. The historical Windows Defender registry name persists despite current Microsoft Defender branding; it is neither an executable location nor a store of detected malware.

## Atomic claim

Groups Microsoft Defender Antivirus machine policy, including cloud engine settings.

Scope: **machine**

## Meaning in system-level logs

Resolve the component child and specific value in a logged target. Operation, result, and data can show policy access, but effective antivirus state or detection requires Defender configuration/status and detection records.

### What the path cannot establish

- The namespace does not show that Defender Antivirus is active or cloud protection enabled.
- It does not identify malware, a scan, a detection, or remediation.

### Applicability

Windows Microsoft Defender Antivirus policy namespace; feature and management availability depend on Windows release, product configuration, and management method. The reviewed descendant is cloud protection policy, not a claim covering all Defender products or platforms.


### Claim-level evidence

- **structural_inference** — Microsoft documents the MpEngine machine policy location beneath Windows Defender and distinguishes cloud protection activation from protection level.
  Section: Specify the cloud protection level with Group Policy.
  - [https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus](<https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus>)

### Explanation sources

- [https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus](<https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: false

- [https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus](<https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus>)

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
