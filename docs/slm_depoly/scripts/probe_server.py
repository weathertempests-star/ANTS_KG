"""Synthetic vLLM checks over loopback or explicit private LAN; not an accuracy benchmark."""

import argparse
import ipaddress
import json
import os
import time
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Unexpected redirect; check the configured server origin")


def validate_origin(origin, allow_lan, api_key):
    url = urlparse(origin)
    if (url.scheme not in {"http", "https"} or url.username or url.password
            or url.path not in {"", "/"} or url.query or url.fragment):
        raise ValueError("Use an HTTP(S) origin without path, credentials, or query")
    host = url.hostname
    if host == "localhost":
        return
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        raise ValueError("Use the server's literal private IP or localhost") from None
    if address.is_loopback:
        return
    networks = [ipaddress.ip_network(n) for n in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "fc00::/7")]
    if not allow_lan or not api_key or not any(address in n for n in networks):
        raise ValueError("Private LAN access requires --allow-lan and SLM_API_KEY_FILE or SLM_API_KEY")


def validate_response(request, response):
    choices = response.get("choices", [])
    if len(choices) != 1 or choices[0].get("finish_reason") != "stop":
        raise ValueError("Expected one completed choice (finish_reason=stop)")
    message = choices[0]["message"]
    if message.get("reasoning_content") or message.get("reasoning"):
        raise ValueError("Thinking was not disabled")
    content = message.get("content")
    if not isinstance(content, str) or not content.strip() or "<think>" in content:
        raise ValueError("Expected non-empty final text without thinking blocks")
    usage = response.get("usage", {})
    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
        if type(usage.get(key)) is not int or usage[key] < 0:
            raise ValueError("Missing or invalid token accounting: " + key)
    if usage["prompt_tokens"] > 4096 or usage["completion_tokens"] > request["max_tokens"]:
        raise ValueError("Request exceeded the pilot token limits")
    if usage["total_tokens"] != usage["prompt_tokens"] + usage["completion_tokens"]:
        raise ValueError("Inconsistent token accounting")
    form = request.get("response_format")
    if form:
        # Full schema validation is provided by jsonschema in the deployment venv.
        import jsonschema
        answer = json.loads(content)
        jsonschema.validate(answer, form["json_schema"]["schema"])
        if "evidence_event_ids" in answer:
            if not set(answer["evidence_event_ids"]) <= {"event_0"}:
                raise ValueError("Invented event reference")
            if not set(answer["knowledge_node_ids"]) <= {"fixture_run_key"}:
                raise ValueError("Invented knowledge reference")
            available = {"event_0", "fixture_run_key"}
            if any(not set(c["evidence_ids"]) <= available for c in answer["claims"]):
                raise ValueError("Invented claim reference")
        if "calls" in answer:
            if any(not set(c["event_ids"]) <= {"event_0"} for c in answer["calls"]):
                raise ValueError("Tool requested an unavailable event")
    return content


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--model", default="registry-slm")
    parser.add_argument("--allow-lan", action="store_true")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--repeat", type=int, default=1, help="Engineering repetition only")
    args = parser.parse_args()
    key_path = os.environ.get("SLM_API_KEY_FILE")
    api_key = Path(key_path).read_text().strip() if key_path else os.environ.get("SLM_API_KEY", "")
    try:
        validate_origin(args.base_url, args.allow_lan, api_key)
    except ValueError as exc:
        parser.error(str(exc))
    if args.repeat < 1:
        parser.error("--repeat must be positive")
    args.out.mkdir(parents=True, exist_ok=True)
    opener = build_opener(ProxyHandler({}), NoRedirect())
    base = args.base_url.rstrip("/")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    # Exclusive output avoids silently replacing an earlier probe result.
    with (args.out / "probe.jsonl").open("x", encoding="utf-8") as report:
        with opener.open(Request(base + "/health", headers=headers), timeout=30) as response:
            if response.status != 200:
                raise RuntimeError("Health endpoint failed")
        with opener.open(Request(base + "/v1/models", headers=headers), timeout=30) as response:
            models = json.load(response)
        if args.model not in {item["id"] for item in models["data"]}:
            raise RuntimeError("Requested model alias is not served")
        fixtures = Path(__file__).resolve().parent.parent / "requests"
        failures = 0
        for iteration in range(args.repeat):
            for path in sorted(fixtures.glob("*.json")):
                request = json.loads(path.read_text())
                request["model"] = args.model
                record = {"fixture": path.name, "iteration": iteration, "request": request,
                          "status": "error", "response": None}
                start = time.perf_counter()
                try:
                    http = Request(base + "/v1/chat/completions",
                                   data=json.dumps(request).encode(),
                                   headers=headers)
                    with opener.open(http, timeout=300) as response:
                        record["response"] = json.load(response)
                    validate_response(request, record["response"])
                    record["status"] = "valid"
                except Exception as exc:
                    record["error"] = str(exc)
                    failures += 1
                record["latency_seconds"] = time.perf_counter() - start
                report.write(json.dumps(record, ensure_ascii=False) + "\n")
                report.flush()
                print(path.name, record["status"], round(record["latency_seconds"], 3))
    if failures:
        raise SystemExit(f"{failures} probes failed; inspect probe.jsonl (no automatic retries)")
    print("PASS: API/schema/reference checks only; no detection accuracy was evaluated")


if __name__ == "__main__":
    main()
