"""Exportable research discussion and a standalone descriptive SVG figure."""

from html import escape


def write_discussion(output, metrics, config, counts):
    engineering = metrics["engineering_only"]
    title = "Engineering validation — not detection performance" if engineering else "Registry KG-assisted evaluation"
    rows = metrics["strata"]["recording_id"]
    height = 85 + 42 * len(rows)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" role="img">',
           '<rect width="100%" height="100%" fill="white"/>',
           f'<text x="20" y="25" font-family="sans-serif" font-size="16">{escape(title)}</text>',
           '<text x="380" y="50" font-family="sans-serif" font-size="12">BA_all (0–1); unresolved remain in denominators</text>']
    for index, (name, values) in enumerate(rows.items()):
        y = 75 + index * 42
        value = values["BA_all"]
        label = "N/A (single truth class)" if value is None else f"{value:.4f}"
        svg.extend([f'<text x="20" y="{y}" font-family="sans-serif" font-size="12">{escape(name)}</text>',
                    f'<rect x="380" y="{y-14}" width="400" height="18" fill="#eee"/>'])
        if value is not None:
            svg.append(f'<rect x="380" y="{y-14}" width="{400*value:.3f}" height="18" fill="#3268a8"/>')
        svg.append(f'<text x="790" y="{y}" font-family="sans-serif" font-size="12">{label}</text>')
    svg.append('</svg>')
    (output / "per_recording_ba.svg").write_text("\n".join(svg), encoding="utf-8")
    text = f"# {title}\n\n"
    text += "## Research question\n\nDoes fixed Registry functional knowledge improve event judgments under the same targets, evidence scope, and inference budget? A single run cannot establish a KG or agent advantage.\n\n"
    text += "## Design\n\n"
    text += f"Condition: `{config['configuration']['condition']}`. Config identity: `{config['config_hash']}`. "
    text += "The model runs on Spark; retrieval, bounded tool execution, and independent evaluation run on the client. "
    text += "Manual labels are per event; recorded timestamps supply only ordering, never elapsed duration.\n\n"
    text += "## Results\n\n| Metric | Weighted value |\n|---|---:|\n"
    for key in ("BA_all", "macro_F1", "malicious_recall", "FPR", "coverage"):
        value = metrics["weighted"][key]
        text += f"| {key} | {value if value is not None else 'N/A'} |\n"
    text += "\n![Per-recording balanced class recall](per_recording_ba.svg)\n\n"
    text += "Raw outcome counts: " + ", ".join(f"{key}={counts[key]}" for key in ("TP", "TN", "FP", "FN", "unresolved")) + ". "
    text += "Inspect [the local case report](report.html) for the actually delivered evidence, predictions, and failure cases. Missing categories have no fabricated examples.\n\n"
    text += "## Limits and next comparisons\n\n"
    if engineering:
        text += "This run is engineering-only. Synthetic outputs or a limited smoke-test target set do not measure detector quality.\n\n"
    text += "Unresolved predictions remain in denominators. Single-class BA is undefined. Sampling-adjusted metrics estimate an event distribution, not deployment performance on unseen hosts. "
    text += "A functional description does not establish malicious intent, operation success, or a causal attack chain. ID-valid citations still need human support review. "
    text += "Use paired target-matched controls and dependency-block uncertainty before attributing improvement to KG, graph representation, or autonomous retrieval. "
    text += "Report retrieval coverage, key/value uncertainty, duplicate sensitivity, measured cost, and negative findings alongside quality.\n"
    (output / "EXPERIMENT_REPORT.md").write_text(text, encoding="utf-8")
