"""Command registration; domain logic lives in focused modules."""

import argparse
import json


def main(argv=None):
    parser = argparse.ArgumentParser(prog="ants-kgmaer", description="Registry KG-assisted research pipeline")
    sub = parser.add_subparsers(dest="command", required=True)
    ingest = sub.add_parser("ingest", help="Verify and ingest a source manifest into separate event/answer stores")
    ingest.add_argument("--sources", required=True)
    ingest.add_argument("--data-root", required=True)
    ingest.add_argument("--labels", required=True)
    ingest.add_argument("--relations", required=True)
    ingest.add_argument("--output", required=True)
    select = sub.add_parser("select", help="Audit overlap, validate recording splits, and sample targets")
    select.add_argument("--dataset", required=True)
    select.add_argument("--output", required=True)
    select.add_argument("--negative-cap", type=int, default=2000)
    select.add_argument("--full", action="store_true")
    select.add_argument("--seed", type=int, default=20261026)
    select.add_argument("--splits")
    run = sub.add_parser("run", help="Execute or resume a frozen model experiment")
    run.add_argument("--config", required=True)
    run.add_argument("--dataset", required=True)
    run.add_argument("--selection", required=True)
    run.add_argument("--output", required=True)
    run.add_argument("--snapshot")
    evaluate = sub.add_parser("evaluate", help="Score all selected targets against separate manual annotations")
    evaluate.add_argument("--dataset", required=True)
    evaluate.add_argument("--selection", required=True)
    evaluate.add_argument("--run", required=True)
    evaluate.add_argument("--output", required=True)
    evaluate.add_argument("--prepared", help="Verified preparation directory for KG-match strata")
    prepare = sub.add_parser("prepare", help="Export contexts, KG cache, and coverage with frozen identities")
    prepare.add_argument("--config", required=True)
    prepare.add_argument("--dataset", required=True)
    prepare.add_argument("--selection", required=True)
    prepare.add_argument("--output", required=True)
    prepare.add_argument("--snapshot")
    population = sub.add_parser("coverage-population", help="Audit every Registry event without model inference")
    population.add_argument("--dataset", required=True)
    population.add_argument("--output", required=True)
    population.add_argument("--snapshot")
    population.add_argument("--template-candidates", action="store_true")
    compare = sub.add_parser("compare", help="Paired dependency-block bootstrap on identical evaluated targets")
    compare.add_argument("--left", required=True)
    compare.add_argument("--right", required=True)
    compare.add_argument("--output", required=True)
    compare.add_argument("--repetitions", type=int, default=2000)
    compare.add_argument("--seed", type=int, default=20261026)
    report = sub.add_parser("report", help="Render an offline HTML metrics and evidence report")
    report.add_argument("--evaluation", required=True)
    report.add_argument("--run", required=True)
    report.add_argument("--output", required=True)
    report.add_argument("--cases-per-type", type=int, default=5)
    duplicates = sub.add_parser("duplicates", help="Observed-group duplicate sensitivity with annotation conflicts isolated")
    duplicates.add_argument("--dataset", required=True)
    duplicates.add_argument("--evaluation", required=True)
    duplicates.add_argument("--output", required=True)
    review_export = sub.add_parser("review-export", help="Sample blinded claim-support review packets")
    review_export.add_argument("--run", required=True)
    review_export.add_argument("--output", required=True)
    review_export.add_argument("--limit", type=int, default=100)
    review_export.add_argument("--seed", type=int, default=20261026)
    review_import = sub.add_parser("review-import", help="Validate human review responses and summarize support")
    review_import.add_argument("--review", required=True)
    review_import.add_argument("--annotations", required=True)
    review_import.add_argument("--output", required=True)
    verify = sub.add_parser("verify", help="Verify required artifact hashes and frozen identities")
    verify.add_argument("directory")
    export = sub.add_parser("export-data", help="Export portable event JSONL and annotation-audit CSV")
    export.add_argument("--dataset", required=True)
    export.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    if args.command == "ingest":
        from .data.ingest import ingest as execute
        result = execute(args.sources, args.data_root, args.labels, args.relations, args.output,
                         progress=lambda item: print(json.dumps(item), flush=True))
    elif args.command == "select":
        from .data.sampling import select_targets
        result = select_targets(args.dataset, args.output, None if args.full else args.negative_cap,
                                args.seed, args.splits)
    elif args.command == "run":
        from .experiments.runner import execute_run
        kwargs = {"snapshot": args.snapshot} if args.snapshot else {}
        result = execute_run(args.config, args.dataset, args.selection, args.output,
                             progress=lambda item: print(json.dumps(item), flush=True), **kwargs)
    elif args.command == "evaluate":
        from .evaluation.scoring import evaluate_run
        result = evaluate_run(args.dataset, args.selection, args.run, args.output, args.prepared)
    elif args.command == "prepare":
        from .experiments.preparation import prepare_inputs
        kwargs = {"snapshot": args.snapshot} if args.snapshot else {}
        result = prepare_inputs(args.config, args.dataset, args.selection, args.output,
                                progress=lambda item: print(json.dumps(item), flush=True), **kwargs)
    elif args.command == "coverage-population":
        from .experiments.population import audit_population
        kwargs = {"snapshot": args.snapshot} if args.snapshot else {}
        result = audit_population(args.dataset, args.output, templates=args.template_candidates,
                                  progress=lambda item: print(json.dumps(item), flush=True), **kwargs)
    elif args.command == "compare":
        from .evaluation.comparison import compare_evaluations
        result = compare_evaluations(args.left, args.right, args.output, args.repetitions, args.seed)
    elif args.command == "report":
        from .presentation.report import render_report
        result = render_report(args.evaluation, args.run, args.output, args.cases_per_type)
    elif args.command == "duplicates":
        from .evaluation.duplicates import duplicate_sensitivity
        result = duplicate_sensitivity(args.dataset, args.evaluation, args.output)
    elif args.command == "review-export":
        from .evaluation.review import export_review
        result = export_review(args.run, args.output, args.limit, args.seed)
    elif args.command == "review-import":
        from .evaluation.review import import_review
        result = import_review(args.review, args.annotations, args.output)
    elif args.command == "verify":
        from .common.artifacts import verify_directory
        result = verify_directory(args.directory)
    elif args.command == "export-data":
        from .data.export import export_dataset
        result = export_dataset(args.dataset, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
