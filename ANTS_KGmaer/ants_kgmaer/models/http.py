"""LAN-only, no-redirect HTTP transport; credentials never enter persisted requests."""

import ipaddress
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from .contracts import InferenceError


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise InferenceError("Model server redirects are disabled", may_have_generated=False)


def check_origin(origin):
    url = urlparse(origin)
    if url.scheme not in {"http", "https"} or url.username or url.password or url.query or url.fragment or url.path not in {"", "/"}:
        raise ValueError("Model endpoint must be an HTTP(S) origin, without credentials or path")
    if url.hostname == "localhost":
        return True
    try:
        ip = ipaddress.ip_address(url.hostname)
    except ValueError:
        raise ValueError("Use a literal private LAN IP or localhost") from None
    allowed = [ipaddress.ip_network(n) for n in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "fc00::/7")]
    if not ip.is_loopback and not any(ip in net for net in allowed):
        raise ValueError("Only loopback/private LAN model servers are permitted")
    return ip.is_loopback


class HttpTransport:
    def __init__(self, origin, key_env="SLM_API_KEY", key_file_env="SLM_API_KEY_FILE", timeout=300):
        loopback = check_origin(origin)
        key_path = os.environ.get(key_file_env)
        self.key = Path(key_path).read_text().strip() if key_path else os.environ.get(key_env, "")
        if not loopback and not self.key:
            raise ValueError("LAN model API requires a key environment variable or key file")
        self.origin = origin.rstrip("/")
        self.timeout = timeout
        self.opener = build_opener(ProxyHandler({}), NoRedirect())

    def request(self, endpoint, payload=None):
        if endpoint not in {"/health", "/v1/models", "/v1/chat/completions", "/tokenize"}:
            raise ValueError("Unsupported inference endpoint")
        headers = {"Content-Type": "application/json"}
        if self.key:
            headers["Authorization"] = "Bearer " + self.key
        data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode()
        request = Request(self.origin + endpoint, data=data, headers=headers)
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                content = response.read()
                return json.loads(content) if content else {}
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise InferenceError(f"HTTP {exc.code}: {body[:2000]}", may_have_generated=exc.code >= 500) from None
        except (URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            raise InferenceError(type(exc).__name__ + ": " + str(exc)) from exc
