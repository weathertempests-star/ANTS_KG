"""SAGA v2 acquisition, archive inspection and evidence-based source grouping.

Never infer benign labels or shared templates from campaign names. The dependency
file is an explicit, reviewable transcription of archive metadata/source evidence.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import random
import zipfile

from .io import digest, fingerprint, rows, write_json
from .store import ingest

SOURCE_URL = 'https://www.saga-cyber.net/dataset'
DOWNLOAD_URL = 'https://drive.usercontent.google.com/download?id=1bFmRdn5Kw1FVOS37dRXCobZZ9UBBjrni&export=download&confirm=t'
OFFICIAL_SHA256 = 'c15e8b985b4cab1d1ebf106e01ce5c14d9b730da5af786167b58778c422992b1'


def inspect_archive(archive, output):
    """Record checksum failures before stopping; never extract unverified bytes."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    actual = digest(archive)
    manifest = dict(dataset='SAGA', version='v2 Complete Evaluation Set',
                    source_url=SOURCE_URL, download_url=DOWNLOAD_URL,
                    official_sha256=OFFICIAL_SHA256, actual_sha256=actual,
                    inspected_at=datetime.now(timezone.utc).isoformat(),
                    acquired_at=datetime.fromtimestamp(Path(archive).stat().st_mtime, timezone.utc).isoformat(),
                    archive_bytes=Path(archive).stat().st_size,
                    checksum_verified=actual == OFFICIAL_SHA256,
                    archive=str(Path(archive).resolve()))
    write_json(output/'source-manifest.json', manifest)
    if actual != OFFICIAL_SHA256:
        raise ValueError('official checksum mismatch; see source-manifest.json; ingestion stopped')
    with zipfile.ZipFile(archive) as z:
        inventory = []
        for item in z.infolist():
            path = Path(item.filename)
            if path.is_absolute() or '..' in path.parts or (item.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError('unsafe archive member: ' + item.filename)
            inventory.append(dict(path=item.filename, bytes=item.file_size, crc=item.CRC))
        write_json(output/'archive-inventory.json', inventory)
        z.extractall(output/'raw')
    manifest['raw_files'] = {str(p.relative_to(output/'raw')): digest(p)
                             for p in sorted((output/'raw').rglob('*')) if p.is_file()}
    write_json(output/'source-manifest.json', manifest)
    return manifest


def dependency_split(recordings, evidence, duplicate_pairs=(), seed=17):
    """Connected components, including mixed provenance and confirmed duplicates."""
    ids = sorted(r['id'] for r in recordings)
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate recording ID')
    parent = {i: i for i in ids}

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a, b):
        if a not in parent or b not in parent:
            raise ValueError('dependency references unknown recording')
        parent[root(a)] = root(b)

    owners = {}
    complete = True
    for rid in ids:
        item = evidence.get(rid, {})
        complete &= all(item.get(k) for k in ('templates', 'backgrounds', 'fragments'))
        for kind in ('templates', 'backgrounds', 'fragments'):
            for token in item.get(kind, []):
                key = kind, token
                if key in owners:
                    union(rid, owners[key])
                owners[key] = rid
        for component in item.get('components', []):
            union(rid, component)
        if item.get('mixed') and not item.get('components'):
            raise ValueError('mixed campaign components unresolved: ' + rid)
    for a, b in duplicate_pairs:
        union(a, b)
    components = defaultdict(list)
    for rid in ids:
        components[root(rid)].append(rid)
    groups = {'source-' + fingerprint(sorted(v))[:16]: sorted(v) for v in components.values()}
    keys = sorted(groups)
    random.Random(seed).shuffle(keys)
    result = dict(seed=seed, groups=groups, protocol='custom internal SAGA v2 split',
                  scope='source dependencies' if complete else 'recording-level feasibility; template/background reuse not excluded',
                  viable=len(keys) >= 3, splits={})
    if len(keys) < 3:
        result['stop_reason'] = 'fewer than three separable source dependency groups'
        return result
    train_n = min(len(keys)-2, max(1, round(.70*len(keys))))
    validation_n = min(len(keys)-train_n-1, max(1, round(.15*len(keys))))
    for i, key in enumerate(keys):
        result['splits'][key] = 'train' if i < train_n else 'validation' if i < train_n+validation_n else 'test'
    return result


def audit_release(raw_root, output):
    """Full streaming event/label census; metadata gaps block formal comparison."""
    from .classification.data import parse_label
    root = Path(raw_root)
    metadata = json.loads((root/'metadata.json').read_text())
    metadata_by_id = {r['campaign']: r for r in metadata}
    results = []
    for path in sorted((root/'Complete Evaluation Set').glob('*.json')):
        counts, labels, types, operations = Counter(), Counter(), Counter(), Counter()
        fields, identities, examples = set(), Counter(), {}
        for index, event in enumerate(rows(path, 'jsonl')):
            if not isinstance(event, dict) or not {'srcNode', 'dstNode', 'relation', 'timestamp'} <= event.keys():
                raise ValueError(f'unsupported event schema {path}:{index}')
            counts['events'] += 1
            fields.update(event)
            label = parse_label(event.get('label'))
            counts[label['status']] += 1
            labels[str(label['raw'])] += 1
            operations[event['relation']] += 1
            for side in ('srcNode', 'dstNode'):
                node = event[side]
                types[str(node.get('Type')) if node else 'Missing'] += 1
                identities['missing_uuid'] += not bool(node and node.get('UUID'))
            counts['registry_events'] += bool(event['dstNode'] and event['dstNode'].get('Type') == 'Registry')
            if label['status'] not in examples:
                examples[label['status']] = dict(row=index, raw_sha256=fingerprint(event),
                                                fields=sorted(event), raw_label=label['raw'])
        expected = metadata_by_id.get(path.stem, {}).get('event')
        expected = int(str(expected).replace(',', '')) if expected is not None else None
        results.append(dict(id=path.stem, path=str(path.relative_to(root)), sha256=digest(path),
                            format='jsonl', counts=counts, labels=labels, node_types=types,
                            operations=operations, fields=sorted(fields), identity_audit=identities,
                            examples=examples, metadata_events=expected,
                            metadata_count_matches=expected == counts['events']))
        print(json.dumps(dict(recording=path.stem, **counts)), flush=True)
    missing = sorted(r['id'] for r in results if r['id'] not in metadata_by_id)
    report = dict(recordings=results, metadata_sha256=digest(root/'metadata.json'),
                  metadata_fields=sorted({k for r in metadata for k in r}),
                  metadata_missing_recordings=missing,
                  dependency_mapping_available=False,
                  formal_comparison_ready=False,
                  stop_reason='Archive metadata does not map mixed components, templates, fragments or backgrounds; obtain reviewed provenance before full-v2 comparison',
                  scope='schema and label audit only; no held-out model results')
    write_json(output, report)
    return report


def build_sources(raw_root, specification, output):
    """Validate a reviewed schema/file inventory, without rewriting raw evidence.

    specification: recordings [{id,path,format}], dependencies {id: {...}}.
    Event shape must be the observed srcNode/dstNode/relation/timestamp schema.
    Metadata files are hashed alongside the reviewed transcription.
    """
    root = Path(raw_root).resolve()
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    sources, audits = [], []
    for source in specification['recordings']:
        path = (root/source['path']).resolve()
        if not path.is_relative_to(root):
            raise ValueError('source escapes raw directory')
        counts, keys, kinds, operations, labels = Counter(), Counter(), Counter(), Counter(), Counter()
        for index, event in enumerate(rows(path, source['format'])):
            if not isinstance(event, dict) or not {'srcNode', 'dstNode', 'relation', 'timestamp'} <= event.keys():
                raise ValueError(f'unsupported SAGA event schema: {path}:{index}')
            keys.update(event.keys())
            for side in ('srcNode', 'dstNode'):
                node = event[side]
                if node is not None and not isinstance(node, dict):
                    raise ValueError('non-object endpoint')
                if node:
                    kinds[str(node.get('Type'))] += 1
                    counts['missing_uuid'] += not bool(node.get('UUID'))
            counts['events'] += 1
            labels[str(event.get('label'))] += 1
            operations[str(event['relation'])] += 1
        sources.append(dict(source, sha256=digest(path), expected_records=counts['events'], dataset='SAGA-v2'))
        audits.append(dict(id=source['id'], fields=keys, node_types=kinds, operations=operations,
                           labels=labels, counts=counts, position='zero-based parsed event index; raw_sha in SQLite'))
    split = dependency_split(sources, specification.get('dependencies', {}),
                             specification.get('confirmed_duplicate_pairs', []))
    write_json(output/'split-manifest.json', split)
    write_json(output/'schema-audit.json', audits)
    write_json(output/'reviewed-specification.json', specification)
    if not split['viable']:
        raise ValueError(split['stop_reason'])
    group_by_id = {rid: group for group, ids in split['groups'].items() for rid in ids}
    for source in sources:
        source['dependency_group'] = group_by_id[source['id']]
        source['dependency_scope'] = split['scope']
    for name in specification.get('metadata_files', []):
        if not (root/name).resolve().is_relative_to(root):
            raise ValueError('metadata escapes raw directory')
    manifest = dict(dataset='SAGA-v2', recordings=sources, dependency_scope=split['scope'],
                    metadata_sha256={p: digest(root/p) for p in specification.get('metadata_files', [])})
    write_json(output/'sources.json', manifest)
    write_json(output/'splits.json', split['splits'])
    ingest(root, manifest, output/'events.sqlite')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('inspect')
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p = sub.add_parser('audit')
    p.add_argument('--raw', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p = sub.add_parser('ingest')
    p.add_argument('--raw', type=Path, required=True)
    p.add_argument('--specification', type=Path, required=True)
    p.add_argument('--source-manifest', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'inspect':
        inspect_archive(args.archive, args.output)
    elif args.command == 'audit':
        audit_release(args.raw, args.output)
    else:
        acquisition = json.loads(args.source_manifest.read_text())
        if not acquisition.get('checksum_verified') or acquisition['actual_sha256'] != OFFICIAL_SHA256:
            raise ValueError('verified official archive manifest required')
        for name, expected in acquisition['raw_files'].items():
            path = (args.raw/name).resolve()
            if not path.is_relative_to(args.raw.resolve()) or digest(path) != expected:
                raise ValueError('raw file provenance mismatch: ' + name)
        specification = json.loads(args.specification.read_text())
        if any(r['path'] not in acquisition['raw_files'] for r in specification['recordings']):
            raise ValueError('recording is not in verified SAGA archive')
        metadata_ids = {r['campaign'] for r in json.loads((args.raw/'metadata.json').read_text())}
        unresolved = [r['id'] for r in specification['recordings'] if r['id'] not in metadata_ids
                      and not specification.get('dependencies', {}).get(r['id'], {}).get('components')]
        if unresolved:
            raise ValueError('recordings absent from metadata require reviewed component provenance: ' + ', '.join(unresolved))
        build_sources(args.raw, specification, args.output)
        write_json(args.output/'source-manifest.json', acquisition)


if __name__ == '__main__':
    main()
