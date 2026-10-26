"""Build and validate a prompt-only Registry evaluation package.

The authored case file remains the review source. Model runners receive prompts.jsonl;
scorers receive answer-key.jsonl. Keeping those roles separate prevents accidental
answer leakage while preserving a reproducible, inspectable benchmark package.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from standardizer_pkg.zettelkasten import _atomic_write

PROMPT_SCHEMA = "registry-evaluation-prompt-1"
ANSWER_SCHEMA = "registry-evaluation-answer-key-1"
PACKAGE_SCHEMA = "registry-evaluation-package-1"
CASE_FIELDS = {"id", "origin", "question", "supplied_facts", "expected_propositions",
               "prohibited_inferences", "knowledge_paths", "sources", "applicable_dimensions"}


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def _jsonl(values):
    return "".join(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n" for value in values)


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def render_evaluation(cases_path, rubric_path):
    cases_text = Path(cases_path).read_text(encoding="utf-8")
    rubric_text = Path(rubric_path).read_text(encoding="utf-8")
    cases = [json.loads(line) for line in cases_text.splitlines() if line.strip()]
    rubric = json.loads(rubric_text)
    if rubric.get("schema") != "registry-evaluation-rubric-1" or not isinstance(rubric.get("dimensions"), dict):
        raise ValueError("unsupported evaluation rubric")
    dimensions = set(rubric["dimensions"])
    seen = set()
    prompts, answers = [], []
    for case in cases:
        if not isinstance(case, dict) or set(case) != CASE_FIELDS:
            raise ValueError("unexpected or missing evaluation case fields")
        case_id = case["id"]
        if not isinstance(case_id, str) or not re.fullmatch(r"[a-z][a-z0-9_]+", case_id) or case_id in seen:
            raise ValueError("evaluation case IDs must be unique lower_snake_case")
        seen.add(case_id)
        for field in ("origin", "question"):
            if not isinstance(case[field], str) or not case[field].strip():
                raise ValueError("evaluation case text must be nonempty")
        if not isinstance(case["supplied_facts"], dict):
            raise ValueError("supplied_facts must be an object")
        for field in ("expected_propositions", "prohibited_inferences", "applicable_dimensions"):
            if not isinstance(case[field], list) or not case[field] or any(
                    not isinstance(value, str) or not value.strip() for value in case[field]):
                raise ValueError(field + " must be a nonempty string list")
        if not set(case["applicable_dimensions"]) <= dimensions:
            raise ValueError("case uses an unknown rubric dimension")
        if {value.casefold() for value in case["expected_propositions"]} & {
                value.casefold() for value in case["prohibited_inferences"]}:
            raise ValueError("expected and prohibited propositions overlap")
        if not isinstance(case["knowledge_paths"], list) or any(not isinstance(value, str) for value in case["knowledge_paths"]):
            raise ValueError("knowledge_paths must be a string list")
        if not isinstance(case["sources"], list) or any(
                not isinstance(value, str) or not value.startswith("https://") for value in case["sources"]):
            raise ValueError("evaluation sources must be HTTPS URLs")
        prompts.append({"schema": PROMPT_SCHEMA, "id": case_id, "origin": case["origin"],
                        "question": case["question"], "supplied_facts": case["supplied_facts"],
                        "applicable_dimensions": case["applicable_dimensions"]})
        answers.append({"schema": ANSWER_SCHEMA, "id": case_id,
                        "expected_propositions": case["expected_propositions"],
                        "prohibited_inferences": case["prohibited_inferences"],
                        "knowledge_paths": case["knowledge_paths"], "sources": case["sources"]})
    if not cases:
        raise ValueError("evaluation package cannot be empty")
    files = {"prompts.jsonl": _jsonl(prompts), "answer-key.jsonl": _jsonl(answers)}
    manifest = {"schema": PACKAGE_SCHEMA, "cases": len(cases),
                "source_sha256": {"registry_cases.jsonl": _sha(cases_text), "rubric.json": _sha(rubric_text)},
                "files": {name: _sha(content) for name, content in sorted(files.items())},
                "separation": "prompts.jsonl contains no expected propositions, prohibited inferences, knowledge paths, or sources."}
    files["evaluation-manifest.json"] = _json(manifest)
    return files


def validate_evaluation(directory, cases_path=None, rubric_path=None):
    root = Path(directory)
    cases_path = cases_path or root / "registry_cases.jsonl"
    rubric_path = rubric_path or root / "rubric.json"
    expected = render_evaluation(cases_path, rubric_path)
    for name, content in expected.items():
        path = root / name
        if not path.is_file() or path.read_bytes() != content.encode("utf-8"):
            raise ValueError("evaluation package differs from authored cases: " + name)
    return {"valid": True, "cases": json.loads(expected["evaluation-manifest.json"])["cases"],
            "files": len(expected)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=ROOT / "evaluation/registry_cases.jsonl")
    parser.add_argument("--rubric", type=Path, default=ROOT / "evaluation/rubric.json")
    parser.add_argument("--output", type=Path, default=ROOT / "evaluation")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    if args.validate:
        print(json.dumps(validate_evaluation(args.output, args.cases, args.rubric), indent=2))
        return
    files = render_evaluation(args.cases, args.rubric)
    args.output.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        _atomic_write(args.output / name, content)
    print(json.dumps(validate_evaluation(args.output, args.cases, args.rubric), indent=2))


if __name__ == "__main__":
    main()
