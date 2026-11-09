"""Disk-indexed JSONL supervision. Tensor memory is bounded by one candidate."""
import json
from pathlib import Path
import sqlite3
import tempfile
import torch
from .annotations import targets
from .model import encode


def offset_rows(path):
    with open(path, 'rb') as f:
        while True:
            offset = f.tell()
            line = f.readline()
            if not line:
                break
            if line.strip():
                yield offset, json.loads(line)


class Dataset:
    def __init__(self, graphs, annotations, use_kg=True):
        self.kg_hashes = set()
        self.graphs, self.annotations, self.use_kg = Path(graphs), Path(annotations), use_kg
        if (self.graphs.parent/'.building').exists():
            raise ValueError('candidate preparation incomplete')
        self.temp = tempfile.TemporaryDirectory(prefix='kgraphier-selector-')
        self.db = sqlite3.connect(str(Path(self.temp.name)/'offsets.sqlite'))
        self.db.executescript('CREATE TABLE annotations(id TEXT PRIMARY KEY, offset INTEGER); CREATE TABLE graphs(id TEXT PRIMARY KEY); CREATE TABLE examples(id INTEGER PRIMARY KEY, goff INTEGER, aoff INTEGER, split TEXT, provenance TEXT); CREATE TABLE groups(kind TEXT, id TEXT, split TEXT, PRIMARY KEY(kind,id));')
        try:
            for offset, a in offset_rows(annotations):
                self.db.execute('INSERT INTO annotations VALUES(?,?)',(a['graph_id'],offset))
            with open(annotations,'rb') as af:
                for offset, g in offset_rows(graphs):
                    if g.get('kg_sha256'):
                        self.kg_hashes.add(g['kg_sha256'])
                    if len(self.kg_hashes) > 1:
                        raise ValueError('mixed KG snapshots')
                    self.db.execute('INSERT INTO graphs VALUES(?)',(g['id'],))
                    split = g['split']
                    if split not in {'train','validation','test'}:
                        raise ValueError('unknown split')
                    for kind, value in [('group',g['dependency_group']),('recording',g['recording_sha256'])]:
                        self.check_group(kind,value,split)
                    row = self.db.execute('SELECT offset FROM annotations WHERE id=?',(g['id'],)).fetchone()
                    if row is None:
                        continue
                    af.seek(row[0]); a=json.loads(af.readline())
                    _, weights=targets(a,g)
                    if not sum(weights):
                        continue
                    self.check_group('episode',a['episode_id'],split)
                    self.db.execute('INSERT INTO examples(goff,aoff,split,provenance) VALUES(?,?,?,?)',(offset,row[0],split,a['provenance']))
            orphan=self.db.execute('SELECT id FROM annotations EXCEPT SELECT id FROM graphs LIMIT 1').fetchone()
            if orphan:
                raise ValueError('orphan annotations')
            self.db.commit()
        except BaseException:
            self.close()
            raise

    def check_group(self,kind,value,split):
        row=self.db.execute('SELECT split FROM groups WHERE kind=? AND id=?',(kind,value)).fetchone()
        if row and row[0]!=split:
            raise ValueError(kind+' spans splits')
        self.db.execute('INSERT OR IGNORE INTO groups VALUES(?,?,?)',(kind,value,split))

    def ids(self,split=None):
        query='SELECT id FROM examples'
        return [r[0] for r in self.db.execute(query+' WHERE split=?' if split else query,(split,) if split else ())]

    def item(self,index):
        goff,aoff=self.db.execute('SELECT goff,aoff FROM examples WHERE id=?',(index,)).fetchone()
        with self.graphs.open('rb') as gf, self.annotations.open('rb') as af:
            gf.seek(goff); g=json.loads(gf.readline())
            af.seek(aoff); a=json.loads(af.readline())
        y,w=targets(a,g)
        return g,a,encode(g,self.use_kg),torch.tensor(y),torch.tensor(w)

    def view(self,split=None):
        return View(self,self.ids(split))

    def __iter__(self):
        for index in self.ids():
            yield self.item(index)

    def close(self):
        self.db.close()
        self.temp.cleanup()


class View:
    def __init__(self,dataset,indices):
        self.dataset,self.indices=dataset,indices

    def __len__(self):
        return len(self.indices)

    def __iter__(self):
        for index in self.indices:
            yield self.dataset.item(index)
