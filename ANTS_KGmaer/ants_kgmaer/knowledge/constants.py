"""Snapshot vocabulary preserved from the existing knowledge core."""
import re

SCHEMA = "prefix-knowledge-3"
LEGACY_SNAPSHOT_SCHEMA = "prefix-knowledge-2"
CATALOG_SCHEMA = "prefix-knowledge-1"
DEFINITION_FIELDS = {"domain", "path", "role", "explanation", "explanation_sources",
                     "status", "path_sources", "explicitly_listed", "candidate_tags", "research"}
RESEARCH_FIELDS = {"summary", "scope", "log_context", "cannot_infer", "value_semantics", "applicability", "evidence"}
HIVES = {"hklm": "hkey_local_machine", "hkcu": "hkey_current_user",
         "hku": "hkey_users", "hkcr": "hkey_classes_root", "hkcc": "hkey_current_config"}
NT_NATIVE_SOURCE = "https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/registry-key-object-routines"
GUID_TEMPLATE_NAMES = {"<appid_guid>", "<clsid>", "<iid>", "<productcodeguid>",
                       "<setupclassguid>", "<interfaceclassguid>"}
GUID_COMPONENT = re.compile(r"\{[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}", re.I)
SID_COMPONENT = re.compile(r"s-1-\d+(?:-\d+)+", re.I)


