"""Offline shared-knowledge build, read-only lookup, and Markdown vault tools."""

import argparse
import json
from pathlib import Path
import sys

from .knowledge import KnowledgeBase
from .model_data import FORMAT as MODEL_DATA_FORMAT, export_model_data, validate_model_data
from .zettelkasten import RESERVED, export_vault, validate_vault


def _write(value, output=None):
    text = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if output:
        Path(output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def _distinct(paths):
    resolved = [Path(p).resolve() for p in paths if p is not None]
    if len(resolved) != len(set(resolved)):
        raise ValueError("input and output paths must differ")
    for i, path in enumerate(resolved):
        if path.exists() and any(other.exists() and path.samefile(other) for other in resolved[:i]):
            raise ValueError("input and output files must differ")


def _unmanaged_output(path):
    if path is None:
        return
    output = Path(path).resolve()
    for parent in output.parents:
        manifest = parent / "manifest.json"
        if manifest.is_file():
            relative = output.relative_to(parent)
            if relative.parts[0] in RESERVED:
                raise ValueError("use a separate output path; refresh generated files with knowledge-vault")
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get('schema') == MODEL_DATA_FORMAT and str(relative) in data.get('files', {}):
                raise ValueError("use a separate output path; refresh generated data with knowledge-model-data")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    build = sub.add_parser("knowledge-build", help="merge inventory hierarchy with authored catalog explanations")
    build.add_argument("catalog")
    build.add_argument("--inventory", help="saved Registry inventory JSON; omit for explicit catalog-only graphs")
    build.add_argument("-o", "--output", required=True)
    build.add_argument("--markdown", help="optional single-file graph preview")
    resolve = sub.add_parser("knowledge-resolve", help="read-only exact-prefix lookup; report path and explanation completeness")
    resolve.add_argument("graph")
    resolve.add_argument("domain", choices=("registry", "file", "command"))
    resolve.add_argument("input")
    resolve.add_argument("-o", "--output")
    vault = sub.add_parser("knowledge-vault", help="create or safely refresh shared knowledge Markdown notes")
    vault.add_argument("graph")
    vault.add_argument("-o", "--output", required=True)
    check = sub.add_parser("knowledge-validate-vault", help="detect snapshot, Markdown, manifest and generated-link drift")
    check.add_argument("directory")
    context = sub.add_parser("knowledge-context", help="compact cited Registry context for an external model")
    context.add_argument("graph")
    context.add_argument("input", help="registry key path, with value name supplied separately")
    context.add_argument("--value-name")
    context.add_argument("--path-format", choices=("canonical", "nt_native"), default="canonical",
                         help="explicit input namespace; nt_native maps only \\Registry\\Machine and \\Registry\\User")
    context.add_argument("--template-candidates", action="store_true",
                         help="retrieve constrained template-pattern knowledge without asserting key existence")
    context.add_argument("-o", "--output")
    dataset = sub.add_parser("knowledge-model-data", help="export grouped instruction records and graph data")
    dataset.add_argument("graph")
    dataset.add_argument("-o", "--output", required=True)
    check_data = sub.add_parser("knowledge-validate-model-data", help="check learning exports against the supplied graph")
    check_data.add_argument("graph")
    check_data.add_argument("directory")
    args = parser.parse_args(argv)
    try:
        if args.action == "knowledge-build":
            _distinct([args.catalog, args.inventory, args.output, args.markdown])
            _unmanaged_output(args.output)
            _unmanaged_output(args.markdown)
            kb = KnowledgeBase.load_catalog(args.catalog, args.inventory)
            kb.save(args.output)
            if args.markdown:
                Path(args.markdown).write_text(kb.markdown(), encoding="utf-8")
            _write({"nodes": len(kb.to_dict()["nodes"]), "edges": len(kb.to_dict()["edges"])})
        elif args.action == "knowledge-resolve":
            _distinct([args.graph, args.output])
            _unmanaged_output(args.output)
            _write(KnowledgeBase.load(args.graph).resolve(args.input, args.domain), args.output)
        elif args.action == "knowledge-vault":
            _write(export_vault(KnowledgeBase.load(args.graph), args.output))
        elif args.action == "knowledge-validate-vault":
            _write(validate_vault(args.directory))
        elif args.action == "knowledge-context":
            _distinct([args.graph, args.output])
            _unmanaged_output(args.output)
            _write(KnowledgeBase.load(args.graph).model_context(
                args.input, args.value_name, args.path_format, args.template_candidates), args.output)
        elif args.action == "knowledge-model-data":
            _write(export_model_data(KnowledgeBase.load(args.graph), args.output))
        elif args.action == "knowledge-validate-model-data":
            _write(validate_model_data(KnowledgeBase.load(args.graph), args.directory))
        return 0
    except (ValueError, TypeError, KeyError, OSError) as error:
        print(f"ants-kg: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
