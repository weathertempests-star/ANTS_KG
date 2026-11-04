"""Loopback protocol integration; the HTTP peer is synthetic, never a real SLM."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from threading import Thread
import unittest
from unittest.mock import patch

from ants_kgmaer.common.files import canonical, jsonl, read_json, write_json
from ants_kgmaer.experiments.runner import execute_run
from ants_kgmaer.models.mock import MockAdapter
import test_evaluation


class ProtocolPeer(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send_json(self, value, status=200):
        body = canonical(value).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.server.paths.append(self.path)
        self.send_json({"data": [{"id": "test-slm"}]} if self.path == "/v1/models" else {})

    def do_POST(self):
        self.server.paths.append(self.path)
        self.server.authorization.append(self.headers.get("Authorization"))
        payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if self.path == "/tokenize":
            self.send_json({"count": MockAdapter().count_tokens(payload["messages"])})
        elif self.path == "/v1/chat/completions":
            if self.server.fail_next:
                self.server.fail_next = False
                self.send_json({"error": "synthetic interruption"}, 503)
                return
            reply = MockAdapter().generate(payload["messages"], payload["response_format"]["json_schema"]["schema"], payload["max_tokens"])
            self.send_json({"choices": [{"message": {"content": reply.content}, "finish_reason": reply.finish_reason}],
                            "usage": {"prompt_tokens": reply.prompt_tokens, "completion_tokens": reply.completion_tokens,
                                      "total_tokens": reply.prompt_tokens + reply.completion_tokens}})
        else:
            self.send_json({"error": "unexpected endpoint"}, 404)


class HttpIntegrationTests(unittest.TestCase):
    def setUp(self):
        test_evaluation.EvaluationTests.setUp(self)
        environment = patch.dict(os.environ, {"SLM_API_KEY": "test-only-secret", "SLM_API_KEY_FILE": ""})
        environment.start()
        self.addCleanup(environment.stop)
        try:
            self.server = ThreadingHTTPServer(("127.0.0.1", 0), ProtocolPeer)
        except PermissionError as exc:
            self.skipTest("Host disallows loopback sockets; HTTP integration remains unverified: " + str(exc))
        self.server.paths, self.server.authorization, self.server.fail_next = [], [], False
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        config = read_json(self.config)
        config["engineering_limit"] = 4
        config["model"] = {"backend": "vllm", "base_url": f"http://127.0.0.1:{self.server.server_port}",
                           "served_model": "test-slm", "repo": "synthetic/protocol-fixture", "revision": "a" * 40,
                           "tokenizer_revision": "a" * 40, "image_digest": "fixture@sha256:" + "b" * 64,
                           "precision": "synthetic", "timeout": 5}
        write_json(self.config, config, replace=True)

    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def test_real_transport_tokenization_auth_and_completion(self):
        output = self.root / "http-run"
        manifest = execute_run(self.config, self.dataset, self.selection, output)
        self.assertTrue(manifest["engineering_only"])
        self.assertIn("/health", self.server.paths)
        self.assertIn("/v1/models", self.server.paths)
        self.assertIn("/tokenize", self.server.paths)
        self.assertEqual(self.server.paths.count("/v1/chat/completions"), 4)
        self.assertEqual(set(self.server.authorization), {"Bearer test-only-secret"})
        self.assertEqual({r["status"] for r in jsonl(output / "predictions.jsonl")}, {"abstained"})
        self.assertNotIn("test-only-secret", (output / "prompts.jsonl").read_text())
        usage = read_json(output / "usage.json")
        self.assertEqual(usage["known_reply_latency_seconds"]["count"], 4)
        self.assertGreater(usage["known_reply_latency_seconds"]["p95"], 0)

    def test_http_failure_is_not_retried_or_counted_as_free(self):
        self.server.fail_next = True
        output = self.root / "http-failure"
        execute_run(self.config, self.dataset, self.selection, output)
        records = list(jsonl(output / "predictions.jsonl"))
        failures = [r for r in records if r["status"] == "inference_error"]
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0]["usage"]["unknown_usage_attempts"], 1)
        self.assertEqual(failures[0]["usage"]["unknown_token_upper_bound"], 4608)
        self.assertEqual(self.server.paths.count("/v1/chat/completions"), 4)


if __name__ == "__main__":
    unittest.main()
