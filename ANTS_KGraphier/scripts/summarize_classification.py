"""Summarize a completed classification matrix without selecting on test scores."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import statistics

from ants_kgraphier.classification.data import read_jsonl
from ants_kgraphier.io import digest, write_json


def summarize(data, runs):
    rows = json.loads((runs/'comparison.json').read_text())
    grouped = defaultdict(list)
    for row in rows:
        grouped[row['dataset'],row['mode'],row['kg']].append(row)
    summary=[]
    epochs=[]
    for (dataset,mode,kg), values in sorted(grouped.items()):
        metrics={}
        for name in ('balanced_accuracy','technique_macro_f1','technique_e2e_micro_f1'):
            numbers=[r[name] for r in values if r[name] is not None]
            metrics[name]=dict(mean=statistics.mean(numbers) if numbers else None,
                               std=statistics.pstdev(numbers) if numbers else None,
                               minimum=min(numbers) if numbers else None,maximum=max(numbers) if numbers else None)
        summary.append(dict(dataset=dataset,mode=mode,kg=kg,seeds=[r['seed'] for r in values],metrics=metrics))
        for r in values:
            model=json.loads((Path(r['report']).parent/'model.json').read_text())
            if model.get('history'):
                epochs.append(len(model['history']))
    data_summary={}
    for directory in sorted(data.glob('*/graphs.jsonl')):
        labels={a['graph_id']:a for a in read_jsonl(directory.parent/'labels.jsonl')}
        stats=defaultdict(lambda:dict(graphs=0,positive=0,negative=0,unknown=0,event_counts=Counter(),
                                      truncated=0,techniques=Counter(),unique_positive=0,unique_negative=0))
        seen=defaultdict(set)
        for g in read_jsonl(directory):
            a=labels[g['id']]
            split=g['split']
            s=stats[split]
            s['graphs']+=1
            s['positive']+=a['binary']==1
            s['negative']+=a['binary']==0
            s['unknown']+=a['binary'] is None
            s['event_counts'][len(g['events'])]+=1
            s['truncated']+=g['budget_truncated']
            s['techniques'].update(a['techniques'])
            signature=tuple(sorted(e['event_id'] for e in g['events']))
            if signature not in seen[split]:
                s['unique_positive']+=a['binary']==1
                s['unique_negative']+=a['binary']==0
                seen[split].add(signature)
        for split,s in stats.items():
            s['unique_event_sets']=len(seen[split])
            s['mean_events']=sum(k*v for k,v in s['event_counts'].items())/s['graphs']
            s['minimum_events']=min(s['event_counts'])
            s['maximum_events']=max(s['event_counts'])
        # Every model has the same class dictionary per extraction condition.
        first=next(r for r in rows if r['dataset']==directory.parent.name)
        report=json.loads(Path(first['report']).read_text())
        data_summary[directory.parent.name]=dict(splits=stats,train_classes=report['config']['classes'],
             test_uncovered=report['uncovered_techniques'],test_known_support={t:m['positive'] for t,m in report['technique_oracle']['per_class'].items()})
    manifest=json.loads((data/'manifest.json').read_text())
    audit=json.loads((data/'split-audit.json').read_text())
    return dict(runs=len(rows),prepared_manifest_sha256=digest(data/'manifest.json'),
                comparison_sha256=digest(runs/'comparison.json'),datasets=data_summary,results=summary,
                epochs_observed=sorted(set(epochs)),initial_per_recording=manifest['per_recording'],
                unknown_labels=len(audit['unknown_labels']),cross_split_exact_events=len(audit['cross_split_exact_events']),
                scope='Development smoke only when epochs or initial sampling are below full settings; no unseen-script claim.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data',type=Path,required=True)
    p.add_argument('--runs',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    if (args.runs/'.building').exists() or list(args.runs.glob('*/.building')):
        raise ValueError('unfinished model runs')
    report=summarize(args.data,args.runs)
    write_json(args.output.with_suffix('.json'),report)
    lines=['# 本地固定擷取分類驗證', '',
           f"初始每錄製 {report['initial_per_recording']} 個共同錨點，完成 {report['runs']} runs；實際訓練 epochs 為 {report['epochs_observed']}。",
           '這是跨錄製開發 smoke，不是完整 2,000 錨點／最多 50 epochs 的研究驗收，也不支持未見腳本泛化。', '',
           f"原始標籤格式未知數：{report['unknown_labels']}；跨分割完全相同原始事件：{report['cross_split_exact_events']}。hash 稽核不能排除改名或改時間的腳本重用。", '',
           '## 資料支持與圖大小', '', '| 條件 | Split | 圖數 | 陽性 | 去重事件集合 | 去重陽性 | 平均事件數 | 最小–最大 |',
           '|---|---|---:|---:|---:|---:|---:|---|']
    for name,item in report['datasets'].items():
        for split,s in item['splits'].items():
            lines.append(f"| {name} | {split} | {s['graphs']} | {s['positive']} | {s['unique_event_sets']} | {s['unique_positive']} | {s['mean_events']:.2f} | {s['minimum_events']}–{s['maximum_events']} |")
    lines+=['','## 三 seeds 比較','', '以下為 graph-level binary balanced accuracy 的平均 ± population standard deviation；不是對錄製平均，也不是信賴區間。Technique macro-F1 只含 test 具有正例支持的 train 類別。', '',
            '| 條件 | 模型 | KG | Seeds | Binary BA | Oracle Technique macro-F1 | E2E Technique micro-F1 |',
            '|---|---|---|---|---|---|---|']
    def fmt(m):
        return '不可評估' if m['mean'] is None else f"{m['mean']:.4f} ± {m['std']:.4f}"
    for r in report['results']:
        metrics=r['metrics']
        lines.append(f"| {r['dataset']} | {r['mode']} | {r['kg']} | {r['seeds']} | {fmt(metrics['balanced_accuracy'])} | {fmt(metrics['technique_macro_f1'])} | {fmt(metrics['technique_e2e_micro_f1'])} |")
    lines+=['','## 未覆蓋 Technique 與限制','']
    for name,item in report['datasets'].items():
        lines.append(f"- {name}：test 已知類別支持 `{json.dumps(item['test_known_support'])}`；未覆蓋 `{json.dumps(item['test_uncovered'])}`。")
    lines+=['','validation 由固定順序擴充，不增補惡意錨點；test 清單固定。目前 train 同樣只採均勻錨點，不依惡意標籤增補；來源不同仍可能造成先驗差異。',
            '短訓練及 test 支持不足限制了這張表的解讀；即使某次 GNN 分數較高，仍需完整訓練、跨 seed 穩定性與獨立資料才能作效益結論。',
            '逐類 precision/recall/F1、完整混淆矩陣、各錄製與去重分組、未覆蓋事件數、binary/Technique 錯誤案例在每 run 的 test.json；逐圖機率與 gate 後預測在 predictions.jsonl。', '',
            f"完整本地產物：`{args.data}`、`{args.runs}`。",'']
    args.output.with_suffix('.md').write_text('\n'.join(lines))


if __name__=='__main__':
    main()
