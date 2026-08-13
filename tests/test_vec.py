import pytest

from mnemosine import EmbeddingRequired, VectorError, vec


def _vec_installed():
    try:
        import sqlite_vec  # noqa: F401

        return True
    except Exception:
        return False


@pytest.mark.skipif(not _vec_installed(), reason="sqlite-vec not installed")
def test_knn_ordering(db):
    db.vec.set_vector("n1", [1.0, 0.0, 0.0])
    db.vec.set_vector("n2", [0.0, 1.0, 0.0])
    db.vec.set_vector("n3", [0.0, 0.0, 1.0])
    results = db.vec.knn([1.0, 0.1, 0.0], top_k=2)
    assert [r["node_id"] for r in results] == ["n1", "n2"]
    assert results[0]["distance"] <= results[1]["distance"]


def test_knn_requires_consistent_dims(db):
    db.vec.set_vector("a", [1.0, 2.0, 3.0])
    with pytest.raises(VectorError):
        db.vec.set_vector("b", [1.0, 2.0])


def test_embed_roundtrip(db):
    db.embed_fn = lambda text: [1.0 if "foo" in text else 0.0, 0.0, 1.0]
    doc = db.node(kind="doc")
    doc.content = "foo bar"
    doc.save()
    doc.add_embedding()
    got = db.vec.get_vector(doc.id)
    assert got == [1.0, 0.0, 1.0]
    results = db.search.vector([1.0, 0.0, 1.0], top_k=1)
    assert results[0]["node"].id == doc.id


def test_embed_without_fn_raises(db):
    doc = db.node(kind="doc")
    doc.save()
    with pytest.raises(EmbeddingRequired):
        doc.add_embedding()


def test_embed_requires_text(db):
    db.embed_fn = lambda text: [1.0]
    doc = db.node(kind="doc")
    doc.save()
    with pytest.raises(EmbeddingRequired):
        doc.add_embedding()


def test_vector_delete(db):
    db.embed_fn = lambda text: [1.0, 0.0]
    doc = db.node(kind="doc")
    doc.content = "x"
    doc.save()
    doc.add_embedding()
    assert db.vec.get_vector(doc.id) is not None
    db.vec.delete(doc.id)
    assert db.vec.get_vector(doc.id) is None
    flag = db.conn.execute(
        "SELECT embedding FROM nodes WHERE id = ?", (doc.id,)
    ).fetchone()["embedding"]
    assert flag == 0