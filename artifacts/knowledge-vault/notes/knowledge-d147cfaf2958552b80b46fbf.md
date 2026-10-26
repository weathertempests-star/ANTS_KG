---
node_id: "knowledge:d147cfaf2958552b80b46fbf"
generated: true
---

# DNSClient

## Full prefix

~~~text
HKLM\Software\Policies\Microsoft\Windows NT\DNSClient
~~~

- Domain: registry
- Depth: L6
- Node ID: `knowledge:d147cfaf2958552b80b46fbf`

## Hierarchy

Parent: [Windows NT](knowledge-279dead16457daba15a15074.md)

Children:

None in this inventory.

## Functional explanation

Status: **documented**

Role: dns&#95;client&#95;policy

This machine Windows NT DNSClient policy key controls DNS client behavior, including policy DNS servers, connection-specific suffixes, DNS suffix searching and devolution, dynamic registration, and link-local name resolution. These are settings used when resolving or publishing names, rather than a DNS cache or query history. The computer primary DNS suffix policy is documented at the separate Microsoft System DNSClient location.

## Atomic claim

Stores machine resolver, DNS suffix, dynamic registration, and multicast name-resolution policies.

Scope: **machine**

## Meaning in system-level logs

Inspect the value name and data, operation, and result to distinguish server selection from registration or LLMNR policy. Actual queries, successful resolution, and dynamic DNS updates require resolver, network, or DNS-server evidence.

### What the path cannot establish

- The path does not identify a resolved hostname or prove DNS traffic occurred.
- A configured DNS server is not evidence it answered, and registration policy does not prove a record was published.
- The EnableMulticast name must be interpreted with the inverse wording of the turn-off policy.

### Applicability

The referenced ADMX CSP tables list device scope on Pro, Enterprise, Education, and IoT Enterprise: Windows 10 2004/20H2/21H1 with KB5005101, and Windows 11 21H2 or later. These are CSP delivery baselines; they do not date the introduction of the underlying Group Policy setting.

### Selected values and subkeys

These are documented examples, not an exhaustive schema or observed data.

- **RegisterAdapterName** (value): Controls using connection-specific suffixes for dynamic A/PTR registration when dynamic registration is enabled.
- **EnableMulticast** (value): Controls LLMNR; the corresponding administrative policy is phrased as turning multicast name resolution off.

### Claim-level evidence

- **direct** — The policy DNS server list maps here and supersedes local and DHCP-provided lists.
  Section: DNS&#95;NameServer.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;nameserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_nameserver>)
- **direct** — The connection-specific suffix policy maps here and supersedes local and DHCP suffixes.
  Section: DNS&#95;Domain.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;domain](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_domain>)
- **direct** — RegisterAdapterName controls dynamic registration using connection-specific suffixes and is ignored when dynamic registration is disabled.
  Section: DNS&#95;RegisterAdapterName.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;registeradaptername](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_registeradaptername>)
- **direct** — EnableMulticast maps the policy that disables LLMNR on available network adapters.
  Section: Turn&#95;Off&#95;Multicast.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#turn&#95;off&#95;multicast](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#turn_off_multicast>)

## Related knowledge

Each relation has an explicit meaning; it does not assert identical keys or observed causation.

- **COMPLEMENTARY_DNS_POLICY_LOCATION** (incoming): [DNSClient](knowledge-73129d1644b7f8f197a8c2fb.md)
  Microsoft System DNSClient hosts the computer primary DNS suffix policy; Windows NT DNSClient hosts distinct DNS server, connection-specific suffix, registration, and resolver policies.
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;primarydnssuffix](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_primarydnssuffix>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;domain](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_domain>)
  - [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;nameserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_nameserver>)

### Explanation sources

- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;nameserver](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_nameserver>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;domain](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_domain>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns&#95;registeradaptername](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#dns_registeradaptername>)
- [https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#turn&#95;off&#95;multicast](<https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient#turn_off_multicast>)

## Path evidence

These citations support the path or an ancestor prefix only; they do not establish its function.

Explicitly listed in inventory: true

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

## Templates and candidate tags

- Placeholder component: false
- Template-dependent prefix: false

Candidate tags: `[]`. Tagging has not been performed.

[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)
