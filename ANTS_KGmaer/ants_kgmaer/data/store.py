"""Read-only event access; this class cannot open the separate answer database."""

import json
import sqlite3
from pathlib import Path


EVENT_SCHEMA = """
CREATE TABLE events (
    event_id TEXT PRIMARY KEY, recording_id TEXT NOT NULL, row_index INTEGER NOT NULL,
    actor_id TEXT NOT NULL, order_ref INTEGER, target_type TEXT NOT NULL,
    facts TEXT NOT NULL, exact_signature TEXT NOT NULL, normalized_signature TEXT NOT NULL
);
CREATE TABLE recordings (recording_id TEXT PRIMARY KEY, cohort TEXT, dependency_group TEXT);
"""
EVENT_INDEXES = """
CREATE INDEX event_context ON events(recording_id, actor_id, order_ref, row_index);
CREATE INDEX event_target ON events(target_type, recording_id);
CREATE INDEX event_exact ON events(exact_signature, recording_id);
CREATE INDEX event_normalized ON events(normalized_signature, recording_id);
"""
LABEL_SCHEMA = """
CREATE TABLE labels (event_id TEXT PRIMARY KEY, recording_id TEXT, label_binary INTEGER,
    label_original TEXT, technique TEXT, quarantine_reason TEXT);
CREATE INDEX labels_by_recording ON labels(recording_id, label_binary);
"""


def readonly(path):
    path = Path(path).resolve()
    connection = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only=ON")
    return connection


class EventStore:
    def __init__(self, path):
        self.path = Path(path)
        self.connection = readonly(path)

    def close(self):
        self.connection.close()

    @staticmethod
    def unpack(row):
        if row is None:
            raise KeyError("Unknown event ID")
        result = dict(row)
        result["facts"] = json.loads(result["facts"])
        return result

    def get(self, event_id):
        return self.unpack(self.connection.execute("SELECT * FROM events WHERE event_id=?", (event_id,)).fetchone())

    def prior(self, event, k):
        if type(k) is not int or k < 0 or k > 32:
            raise ValueError("History k must be an integer in [0,32]")
        if not k or event["order_ref"] is None or not event["facts"]["actor_identity_known"]:
            return []
        rows = self.connection.execute(
            "SELECT * FROM events WHERE recording_id=? AND actor_id=? AND order_ref<? "
            "ORDER BY order_ref DESC, row_index DESC LIMIT ?",
            (event["recording_id"], event["actor_id"], event["order_ref"], k),
        ).fetchall()
        return [self.unpack(row) for row in reversed(rows)]

    def registry_ids(self, recording_id=None):
        query = "SELECT event_id FROM events WHERE target_type='Registry'"
        values = ()
        if recording_id:
            query += " AND recording_id=?"
            values = (recording_id,)
        query += " ORDER BY recording_id, row_index"
        for row in self.connection.execute(query, values):
            yield row[0]
