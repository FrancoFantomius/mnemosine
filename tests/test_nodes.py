import pytest

from mnemosine import NodeNotFound


def test_create_and_get(db):
    doc = db.node(kind="doc")
    doc["title"] = "Hello"
    doc["tags"] = ["a", "b"]
    doc.content = "body text"
    doc.save()

    loaded = db.get(doc.id)
    assert loaded.id == doc.id
    assert loaded.kind == "doc"
    assert loaded["title"] == "Hello"
    assert loaded["tags"] == ["a", "b"]
    assert loaded.content == "body text"


def test_update_persists(db):
    doc = db.node(kind="text")
    doc["a"] = 1
    doc.save()
    doc2 = db.get(doc.id)
    doc2["a"] = 2
    doc2["b"] = "x"
    doc2.save()
    doc3 = db.get(doc.id)
    assert doc3["a"] == 2
    assert doc3["b"] == "x"


def test_timestamps_set(db):
    doc = db.node(kind="note")
    doc.save()
    assert doc.created_at
    assert doc.updated_at
    assert db.get(doc.id).created_at == doc.created_at


def test_get_missing_raises(db):
    with pytest.raises(NodeNotFound):
        db.get("nope")


def test_get_missing_default(db):
    assert db.get("nope", default=None) is None


def test_delete(db):
    doc = db.node(kind="text")
    doc.save()
    doc.delete()
    assert not db.exists(doc.id)


def test_refresh(db):
    doc = db.node(kind="text")
    doc["a"] = 1
    doc.save()
    doc["a"] = 999
    doc.refresh()
    assert doc["a"] == 1


def test_list_and_count(db):
    for _ in range(3):
        db.node(kind="doc").save()
    db.node(kind="file").save()
    assert db.count(kind="doc") == 3
    assert db.count() == 4
    assert len(db.list_nodes(kind="doc")) == 3


def test_generated_column_index(db):
    db.node(kind="doc").update(title="First", n=1).save()
    db.node(kind="doc").update(title="Second", n=2).save()
    col = db.index_attribute("n", as_type="INTEGER")
    rows = db.conn.execute(f"SELECT id FROM nodes WHERE {col} > 1").fetchall()
    assert len(rows) == 1