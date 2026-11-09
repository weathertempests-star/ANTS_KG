"""Index the three smallest metadata-listed SAGA recordings for a mechanism pilot.

Selection uses archive byte sizes, never labels. This intentionally excludes
unmapped recordings and cannot establish full-v2 or unseen-template performance.
"""
import argparse
import json
from pathlib import Path

from ants_kgraphier.io import digest, write_json
from ants_kgraphier.saga import OFFICIAL_SHA256, build_sources


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verified', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    acquisition = json.loads((args.verified/'source-manifest.json').read_text())
    if not acquisition.get('checksum_verified') or acquisition['actual_sha256'] != OFFICIAL_SHA256:
        raise ValueError('official verified SAGA v2 archive required')
    raw = args.verified/'raw'
    if digest(raw/'metadata.json') != acquisition['raw_files']['metadata.json']:
        raise ValueError('metadata hash mismatch')
    metadata = json.loads((raw/'metadata.json').read_text())
    ids = {r['campaign'] for r in metadata}
    inventory = json.loads((args.verified/'archive-inventory.json').read_text())
    chosen = sorted([r for r in inventory if Path(r['path']).stem in ids],
                    key=lambda r: (r['bytes'], r['path']))[:3]
    if len(chosen) != 3:
        raise ValueError('three listed recordings required')
    for item in chosen:
        if digest(raw/item['path']) != acquisition['raw_files'][item['path']]:
            raise ValueError('recording hash mismatch')
    spec = dict(recordings=[dict(id=Path(r['path']).stem, path=r['path'], format='jsonl') for r in chosen],
                metadata_files=['metadata.json'], dependencies={},
                scope='mechanism pilot only; three smallest metadata-listed recordings; source reuse not excluded')
    build_sources(raw, spec, args.output)
    write_json(args.output/'source-manifest.json', acquisition)


if __name__ == '__main__':
    main()
