"""Label-independent pseudonymization; never serialize raw node objects."""

import hashlib
import re

HASH = re.compile(r"(?i)(?<![0-9a-f])[0-9a-f]{32,64}(?![0-9a-f])")
USER = re.compile(r"(?i)(\\users\\)([^\\/\s\"]+)")
MARKER = re.compile(r"(?i)(?<![\w])(?:maliciousfiles|evil|caldera|sandcat|apt28|cobaltgroup|gamaredon|higaisa|patchwork)(?![\w])")
UNC_HOST = re.compile(r"(\\\\)([^\\\s]+)")
TECHNIQUE = re.compile(r"\bT\d{4}(?:\.\d{3})?(?:_[A-Za-z0-9-]+)?\b")


class Redactor:
    VERSION = "redaction-1"

    def __init__(self, recording_id):
        self.scope = recording_id
        self.counts = {}

    def token(self, value, kind):
        encoded = (self.scope + "\0" + str(value).casefold()).encode()
        return f"<{kind}_{hashlib.sha256(encoded).hexdigest()[:10]}>"

    def text(self, value):
        if value is None:
            return None
        if not isinstance(value, (str, int, float, bool)):
            return None
        value = str(value)
        for name, pattern, replacement in (
            ("sample_identifier", HASH, lambda m: self.token(m[0], "sample")),
            ("username", USER, lambda m: m[1] + (m[2] if m[2].lower() in {"public", "default", "all users"}
                                                else self.token(m[2], "user"))),
            ("experiment_marker", MARKER, lambda m: "<artifact>"),
            ("host", UNC_HOST, lambda m: m[1] + self.token(m[2], "host")),
            ("annotation_technique", TECHNIQUE, lambda m: "<annotation>"),
        ):
            value, count = pattern.subn(replacement, value)
            self.counts[name] = self.counts.get(name, 0) + count
        return value

    def actor(self, raw):
        return {key.lower(): self.text(raw.get(key)) for key in ("Name", "Image", "Cmdline")}

    def target(self, raw):
        fields = ("Name", "Path", "Image", "Cmdline", "Key", "Dstaddress", "Srcaddress", "Port")
        return {"type": raw.get("Type") if raw.get("Type") in {"Registry", "File", "Process", "Network"} else "Other",
                **{key.lower(): self.text(raw[key]) for key in fields if key in raw}}
