def test_link_roundtrip(db):
    a = db.node(kind="doc").save()
    b = db.node(kind="doc").save()
    link = a.link(b, link_type="relation", metadata={"label": "cites"})
    assert link.source_id == a.id
    assert link.target_id == b.id

    links = db.links(source=a.id)
    assert len(links) == 1
    assert links[0].link_type == "relation"
    assert links[0]["label"] == "cites"


def test_link_is_idempotent(db):
    a = db.node().save()
    b = db.node().save()
    db.link(a, b, "rel")
    db.link(a, b, "rel")
    assert len(db.links(source=a.id)) == 1


def test_neighbors(db):
    a = db.node().save()
    b = db.node().save()
    c = db.node().save()
    db.link(a, b, "friend")
    db.link(c, a, "parent")

    out = a.neighbors(direction="out")
    assert [n["node"].id for n in out] == [b.id]
    both = a.neighbors(direction="both")
    assert {n["node"].id for n in both} == {b.id, c.id}


def test_neighbors_link_type_filter(db):
    a = db.node().save()
    b = db.node().save()
    c = db.node().save()
    db.link(a, b, "friend")
    db.link(a, c, "other")
    friends = a.neighbors(link_type="friend", direction="both")
    assert [n["node"].id for n in friends] == [b.id]


def test_node_links_helper(db):
    a = db.node().save()
    b = db.node().save()
    c = db.node().save()
    db.link(a, b, "out")
    db.link(c, a, "in")
    out = a.links(direction="out")
    assert [l.target_id for l in out] == [b.id]
    inc = a.links(direction="in")
    assert [l.source_id for l in inc] == [c.id]


def test_unlink(db):
    a = db.node().save()
    b = db.node().save()
    db.link(a, b)
    db.unlink(a, b)
    assert db.links(source=a.id) == []


def test_delete_node_cascades_links(db):
    a = db.node().save()
    b = db.node().save()
    db.link(a, b)
    a.delete()
    assert db.links(source=a.id) == []
    assert db.links(target=b.id) == []