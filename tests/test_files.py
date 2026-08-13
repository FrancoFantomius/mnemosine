import io

import pytest

from mnemosine import File, FileNotFound


def test_write_read(db):
    f = db.file("note.txt", mime="text/plain")
    f.write(b"hello world")
    assert f.read() == b"hello world"
    assert f.text() == "hello world"
    assert f.size_bytes == 11
    assert len(f.sha256) == 64
    assert f.mime_type == "text/plain"

    loaded = db.get(f.id)
    assert isinstance(loaded, File)
    assert loaded.read() == b"hello world"
    assert loaded.sha256 == f.sha256
    assert loaded.path == "note.txt"


def test_write_str(db):
    f = db.file("note.txt")
    f.write("hello")
    assert f.text() == "hello"


def test_stream_write(db):
    payload = b"x" * 100000
    f = db.file("big.bin")
    f.write_stream(io.BytesIO(payload), chunk_size=4096)
    assert f.size_bytes == len(payload)
    assert f.read() == payload


def test_dedup_shared_hash(db):
    payload = b"same content"
    a = db.file("a.txt")
    a.write(payload)
    b = db.file("b.txt")
    b.write(payload)
    assert a.sha256 == b.sha256
    assert a._rel_path == b._rel_path


def test_gc_blobs_removes_orphans(db, tmp_path):
    a = db.file("keep.txt")
    a.write(b"keep me")
    blob_path = db.blob_root / a._rel_path
    assert blob_path.exists()

    orphan = db.blob_root / "blobs" / "zz" / "deadbeef"
    orphan.parent.mkdir(parents=True, exist_ok=True)
    orphan.write_bytes(b"orphan")

    a.delete()  # removes the blob row but not the file on disk
    assert blob_path.exists()

    removed = db.gc_blobs()
    assert removed >= 2
    assert not blob_path.exists()
    assert not orphan.exists()


def test_delete_removes_blob_row(db):
    f = db.file("x.bin")
    f.write(b"data")
    f.delete()
    row = db.conn.execute(
        "SELECT 1 FROM blobs WHERE node_id = ?", (f.id,)
    ).fetchone()
    assert row is None


def test_read_before_write_raises(db):
    f = db.file("empty.txt")
    f.save()
    with pytest.raises(FileNotFound):
        f.read()