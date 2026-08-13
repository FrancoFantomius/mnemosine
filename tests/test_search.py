def test_text_search_content(db):
    a = db.node(kind="doc")
    a.content = "the quick brown fox"
    a.save()
    b = db.node(kind="doc")
    b.content = "a lazy dog"
    b.save()
    hits = db.search.text("quick")
    assert len(hits) == 1
    assert hits[0].id == a.id


def test_text_search_metadata(db):
    db.node(kind="doc").update(title="Project Plan").save()
    db.node(kind="doc").update(title="Other").save()
    assert len(db.search.text("Plan")) == 1


def test_text_search_kind_filter(db):
    db.node(kind="doc").update(content="unique term").save()
    db.node(kind="file").update(content="unique term").save()
    assert len(db.search.text("unique", kind="doc")) == 1


def test_like_wildcards_escaped(db):
    db.node().update(content="progress 100% done").save()
    db.node().update(content="progress done").save()
    assert len(db.search.text("100%")) == 1


def test_bad_field_raises(db):
    import pytest

    with pytest.raises(ValueError):
        db.search.text("x", fields=("nope",))