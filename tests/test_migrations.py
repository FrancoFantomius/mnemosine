import sqlite3

from mnemosine import Storage
from mnemosine.migrations import latest_version, migrate


def test_fresh_db_reaches_latest(db):
    version = db.conn.execute("PRAGMA user_version").fetchone()[0]
    assert version == latest_version()


def test_migrate_idempotent(db):
    migrate(db.conn)
    version = db.conn.execute("PRAGMA user_version").fetchone()[0]
    assert version == latest_version()


def test_upgrade_from_zero(tmp_path):
    path = tmp_path / "old.db"
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA user_version = 0")
    conn.commit()
    conn.close()

    store = Storage(path, blob_root=tmp_path / "b")
    store.connect()
    tables = {
        r[0]
        for r in store.conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }
    assert {"nodes", "node_links", "blobs"} <= tables
    version = store.conn.execute("PRAGMA user_version").fetchone()[0]
    assert version == latest_version()
    store.close()


def test_connect_is_idempotent(tmp_path):
    store = Storage(tmp_path / "x.db")
    store.connect()
    conn = store.conn
    store.connect()
    assert store.conn is conn
    store.close()