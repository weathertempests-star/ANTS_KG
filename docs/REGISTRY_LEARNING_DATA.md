# Registry knowledge for readers and models

這份資料把「這個 Registry 位置負責什麼」與「某筆 log 證明發生什麼」分開。197 個節點沿用既有 inventory，每個完整前綴有一篇可引用的英文筆記；功能說明、適用條件、值或子鍵範例、來源與推論限制一起提供。它適合知識檢索與小規模訓練實驗；本批沒有訓練模型，也沒有測得模型效能提升。

## Reading a note

Read the full prefix first. The final name alone is insufficient: `System` under machine startup configuration differs from `System` under a software policy branch. Then read the atomic claim, functional explanation, scope, applicability, and evidence. `documented` means a direct source supports the authored role; `structural` means the namespace role is explicitly inferred from documented descendants. Neither status is an observation of a host.

The hierarchy provides context. The separate semantic links explain specific relationships such as a merged view, a user/machine counterpart, or a client/server distinction. Their explanations and citations are part of the relationship; an edge is not a claim of physical-key identity or causation. This makes the vault a collection of individually addressable knowledge notes with meaningful connections, rather than a list of event instances.

| Term | Meaning here |
|---|---|
| Key / prefix | A named container and its complete location in the Registry hierarchy. |
| Value | A separately named item with type and data inside a key; it is not automatically another key node. |
| Unnamed value | Represented by `name=""`; the UI label “(Default)” is not its actual name. |
| Hive / logical root | The location or view determining context; HKCU depends on the user context, HKCR is a merged view. |
| Policy | Configuration consumed by a component, subject to that setting's scope, precedence and applicability. |
| ADMX / CSP | Administrative-template policy and its management interface; a CSP support table does not date the Registry key's introduction. |
| Template | A documented pattern such as `<ServiceName>`; optional constrained matching yields candidate knowledge, not instance existence. |
| SACL | An object's system access-control list, used with audit policy to determine auditing. |
| Operation / outcome | Facts supplied by a particular event provider; a handle request differs from a completed modification. |

These distinctions are grounded in each note's citations and the [provider interpretation guide](../knowledge/registry_log_semantics.json). The empty-name convention follows the documented [RegQueryValueEx parameter contract](https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regqueryvalueexa).

## Retrieval contract

```bash
python -m standardizer_pkg knowledge-context artifacts/knowledge-vault/kg.json \
  'HKLM\SYSTEM\CurrentControlSet\Control\Session Manager' \
  --value-name PendingFileRenameOperations
```

The response includes cited prefix knowledge, evidence status, scope and applicability, exact named-value knowledge when available, unknown suffixes, and semantic links. `None` (omitted flag) means no value was supplied; `--value-name ''` selects an unnamed value. An empty value-knowledge result means the catalog lacks an exact selected value definition, not that the value cannot exist. Collections of arbitrary named entries remain described as collections.

Supply the **key** path separately from the value name. For documented kernel paths, pass `path_format="nt_native"`: `\Registry\Machine` maps to HKLM and `\Registry\User` maps to HKU while retaining the SID. The adapter deliberately has no HKCU shortcut and does not guess value boundaries or WOW64 views. The mapping follows Microsoft's [kernel Registry root documentation](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/registry-key-object-routines).

Template retrieval is opt-in with `template_candidates=True` or `--template-candidates`. Component-bound matching constrains known SID, braced GUID and extension placeholders and retains original concrete names in `template_bindings`. `path_complete` remains the exact inventory result; `pattern_complete` reports a complete candidate chain. Neither a candidate nor a literal placeholder proves that a concrete key exists, is loaded, or contains documented example values. Without the option, unknown suffixes stay unknown.

For a model prompt, keep three explicit sections: actual event facts, retrieved knowledge, and the question. Ask for (1) target identity and role, (2) the operation supported by the provider and record, (3) unresolved facts and applicable limits, and (4) supporting sources. The snapshot is knowledge, while the supplied event remains separate input.

For example, an audited value-change record can support a value-modification statement. A path naming `Run` alone supports a statement about logon command registration, not a process-execution conclusion. A Security 4656 success concerns the handle request and does not establish a subsequent write. See [4657](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4657) and [4656](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4656).

## Dataset card

| Property | Description |
|---|---|
| Unit | One authored Registry prefix, with stable domain/full-prefix ID. |
| Coverage | 197 nodes from a cross-version document inventory, 192 hierarchy edges, plus sourced semantic relations. |
| Language | English node explanations and model records; Chinese project entry documentation. |
| Authorship | AI-authored synthesis of primary documentation, reviewed by other agents and the root agent; not independent human annotation. |
| Evidence | Claim-level URL, section, support type, and applicability; separate inventory path evidence. Source review records retain read status/date. |
| Intended use | Retrieval, instruction-tuning pilots, node/text embeddings and graph-learning experiments. |
| Not supplied | Real audit corpus, confirmed host state, malicious/benign labels, automatic tagging, learned embeddings, trained model or measured model results. |
| Original seven | Their explanations and IDs are preserved; new research fields add context and limits. |
| Source handling | Original prose summaries with primary-source links; no full third-party pages bundled. Source pages retain their own terms. |

Generate and validate with:

```bash
python -m standardizer_pkg knowledge-model-data artifacts/knowledge-vault/kg.json \
  -o artifacts/model-data
python -m standardizer_pkg knowledge-validate-model-data artifacts/knowledge-vault/kg.json \
  artifacts/model-data
```

| Output | Use |
|---|---|
| `node-records.jsonl` | Complete explanation/research fields, node ID/index, evidence and split assignment. |
| `sft/{train,validation,test}.jsonl` | Two deterministic tasks per node: explain the prefix; interpret a path with no event facts. `messages` is provider-neutral; remove metadata only when adapting to a trainer. |
| `graph/snapshot.json` | Complete source snapshot, including relation explanations and provenance, for reproducibility. |
| `graph/node-index.json` | Deterministic row-index mapping within this snapshot and split; stable node IDs connect different snapshots. |
| `graph/edge-index.json` | Directed typed edges using integer row indexes; hierarchy and semantic kinds stay separate. |
| `graph/semantic-edges.jsonl` | Full stable-ID semantic edges, with explanations and source URLs. |
| `graph/train-edge-index.json` | Only edges whose two endpoints are training nodes. |
| `graph/edges.csv` | Endpoint IDs, relation/kind and endpoint splits. |
| `splits.json` | Deterministic family grouping, node/example counts and limitations. |
| `audit.json`, `manifest.json` | Structural/content checks and reproducible checksums, not factual truth certificates. |

The 394 instruction examples are projections of 197 knowledge units, not 394 independently researched observations. Their answers deliberately teach positive function plus uncertainty. They do not cover all event-conditioned reasoning; use the separate probes below and collect a real evaluation set before making effectiveness claims. Each record retains source metadata; retrieve the complete research record when checking individual claims.

Splits group concept families across hive scopes and template variants, then deterministically assign whole families. The family heuristic is partition metadata, not a functional taxonomy or an attack tag. Related concepts, ancestors and documentation can still overlap across splits. Full graph and node files include held-out material and are explicitly **transductive**. For an inductive experiment, select training node records and use `train-edge-index.json`; never train on all node text or source snapshots while claiming held-out text isolation. Fit any vocabulary, encoder adaptation and feature transforms on the permitted training material only. No benchmark generalization claim follows from this small split.

Refresh verifies the old dataset against its own stored snapshot before writing. Manually edited generated files, changed manifests, symlink targets and unexpected managed-file paths are rejected; unrelated personal files survive. Keep hand-written notes outside managed files. As with the vault, writes are atomic per file, not an all-directory transaction; readers should validate after a refresh completes.

## Evaluation protocol

[Seventeen authored probes](../evaluation/registry_cases.jsonl) include positive event-supported conclusions and tempting but unsupported inferences. They distinguish handle requests, value changes, object creation, renames, key/value names, native namespace adaptation, template uncertainty, scope and legacy policy limitations. They contain **synthetic teaching facts**, never observed host events, and are not inserted into the KG.

Use the [scoring rubric](../evaluation/rubric.json) to assess identity, functional meaning, event calibration, and evidence/applicability. Score only each case's applicable dimensions; N/A dimensions are excluded from the denominator. A supported operation should be explained; blanket refusal is not a correct answer. Any prohibited inference asserted as fact fails a case. Keep expected answers and rubric annotations out of the model prompt and training data.

Build the evaluation package with `python scripts/prepare_registry_evaluation.py`. Give only `prompts.jsonl` to the model runner and keep `answer-key.jsonl` scorer-only; `evaluation-manifest.json` binds both projections to the authored cases and rubric by SHA-256. Validate with `python scripts/prepare_registry_evaluation.py --validate` before a run.

For repository-specific adapter/template questions, provide the same implementation contract to both conditions. Compare identical inputs under raw-input and KG-retrieval conditions, recording model/version, decoding settings, retrieved node IDs and complete responses. Use blinded human review with adjudication before reporting scores. The probes share knowledge with the corpus and are not an independent real-world test set. A later evaluation needs separately collected logs, provider versions, Windows baselines, operation outcomes and appropriate data permissions.

## Maintenance and limits

Edit reviewed research batches and source records, rerun the assembly gate, then rebuild the graph, vault and model data together. Review reports live in [knowledge/research/reviews](../knowledge/research/reviews/). Do not treat a source's mention of a path as support for every function assigned to it. Structural grouping stays visibly inferred; selected values are examples, not an exhaustive schema.

Run `python scripts/audit_registry_research.py --as-of YYYY-MM-DD -o knowledge/research/research_audit.json` after changing research, retrieval, model-data or evaluation artifacts. The audit reassembles the catalog, compares the saved graph, validates vault/model/evaluation manifests, checks exact peer coverage and split isolation, and reports citation-review age. Decide an acceptable maximum age in the study protocol and refresh the affected primary-source reviews before a time-sensitive release. A passing audit establishes internal traceability for the declared scope, not source permanence or factual truth.

The current inventory spans multiple Windows generations. Some policies are obsolete, some operate only with particular roles or consumers, and a registry change need not imply effective enforcement. More source-grounded knowledge can improve a retrieval system's inputs; improvement in any external SLM remains an empirical question until that model is evaluated.
