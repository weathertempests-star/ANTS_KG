"""Generate a research summary from actual manifests, not expected results."""
import argparse
import json
from pathlib import Path
from statistics import mean, median

from ants_kgraphier.io import digest, jsonl, write_json

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--research", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        p.error("output already exists")
    table, timings, extraction, evidence = [], [], [], []
    for method in ("window", "temporal"):
        folder = args.research / method
        manifest = json.loads((folder / "manifest.json").read_text())
        validation = json.loads((folder / "validation.json").read_text())
        if digest(folder / "graphs.jsonl") != manifest["graphs_sha256"]:
            raise ValueError("candidate hash mismatch")
        graphs = list(jsonl(folder / "graphs.jsonl"))
        if validation["validated"] != len(graphs):
            raise ValueError("not all candidates validated")
        extraction.append({"method": method, "candidates": len(graphs),
                           "mean_events": mean(len(g["events"]) for g in graphs),
                           "clipped": sum(g["budget_truncated"] for g in graphs),
                           "extraction_seconds": manifest["seconds"]})
        for name in ("model-no-kg", "model-kg"):
            model = folder / name
            evaluation = json.loads((model / "evaluation.json").read_text())
            config = json.loads((model / "model.json").read_text())
            index = json.loads((model / "index/manifest.json").read_text())
            if digest(model / "weights.pt") != config["weights_sha256"]:
                raise ValueError("model hash mismatch")
            if digest(model / "index/embeddings.npy") != index["embeddings_sha256"]:
                raise ValueError("index hash mismatch")
            if evaluation["index_manifest"] != index:
                raise ValueError("evaluation does not match index")
            table.append({"extractor": method, "model": name,
                          **evaluation["summary"]["provg_order"]})
            if name == "model-kg":
                table.append({"extractor": method, "model": "feature-count baseline",
                              **evaluation["summary"]["feature_count"]})
            timings.append({"extractor": method, "model": name,
                            "train_seconds": config["seconds"], "index_seconds": index["seconds"],
                            "median_query_encode_ms": median(q["query_encoding_seconds"] for q in evaluation["queries"]) * 1000,
                            "median_vector_scan_ms": median(q["vector_scan_seconds"] for q in evaluation["queries"]) * 1000,
                            "median_exact_gallery_ms": median(q["exact_seconds"] for q in evaluation["queries"]) * 1000})
            evidence.append({"path": str(model / "evaluation.json"), "sha256": digest(model / "evaluation.json"),
                             "gallery_size": evaluation["gallery_size"], "queries": evaluation["query_count"]})
    result = {"results": table, "timings": timings, "extraction": extraction, "evidence": evidence,
              "limitations": ["One training seed and 30 synthetic queries per extractor; no confidence claim.",
                              "Queries differ between extractors; cross-extractor scores do not establish segmentation superiority.",
                              "Window reaches at most 17 events; temporal at most 33 under these settings. Context exposure differs.",
                              "No analyst-reviewed relevance or context-completeness labels.",
                              "Feature-count baseline outperforms learned models in this run."]}
    write_json(args.output, result)
    md = ["# 真實資料研究實作驗證\n", "本報告由實際 manifest／checkpoint／evaluation 產生，並核對 hash。\n",
          "| 擷取器 | 模型 | Recall@10 | Recall@50 | MRR |", "|---|---|---:|---:|---:|"]
    for row in table:
        md.append(f"| {row['extractor']} | {row['model']} | {row['recall@10']:.4f} | {row['recall@50']:.4f} | {row['reciprocal_rank']:.4f} |")
    md += ["\n## 擷取成本\n", "| 方法 | 候選數 | 平均事件數 | 達擴展／大小限制 | 擷取秒數 |", "|---|---:|---:|---:|---:|"]
    for row in extraction:
        md.append(f"| {row['method']} | {row['candidates']} | {row['mean_events']:.2f} | {row['clipped']} | {row['extraction_seconds']:.2f} |")
    md += ["\n## 執行時間\n", "向量／精確查詢時間對應 300 個保留候選的 gallery。離線索引對應全部 4,400 個候選。\n",
           "| 方法 | 模型 | 訓練秒 | 索引秒 | 查詢編碼中位 ms | 向量掃描中位 ms | 精確 gallery 搜尋中位 ms |",
           "|---|---|---:|---:|---:|---:|---:|"]
    for row in timings:
        md.append(f"| {row['extractor']} | {row['model']} | {row['train_seconds']:.2f} | {row['index_seconds']:.2f} | {row['median_query_encode_ms']:.3f} | {row['median_vector_scan_ms']:.3f} | {row['median_exact_gallery_ms']:.3f} |")
    md += ["\n## 解讀\n", "KG 在本輪改善兩種擷取器的 Recall@10／Recall@50，但不代表每項指標都改善，且仍落後 feature-count baseline。不能宣稱 GNN 較佳或 KG 拓譜創新已成立。",
           "\n兩種擷取器使用相同錨點，但產生的 query／候選上下文不同，且實際圖大小不同；跨擷取器分數不能當成公平的切圖品質勝負。大量候選觸及擴展限制，下一步應加入獨立的必要上下文標註及固定大小對照。",
           "\n本輪是單 seed 的結構檢索 pilot。合成 query 來源候選仍在 gallery，未證明未知行為或人工調查效益。正式研究需要獨立開發／測試查詢、人工相關性、重複群組分析及多 seed。此輪結果已檢視，後續調參須使用新的保留測試。"]
    args.output.with_suffix(".md").write_text("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
