def test_path_through_chain(db):
    a, b, c = db.node().save(), db.node().save(), db.node().save()
    db.link(a, b)
    db.link(b, c)
    route = db.graph.path(a, c)
    assert [n.id for n in route] == [a.id, b.id, c.id]


def test_path_cycle_safe(db):
    a, b = db.node().save(), db.node().save()
    db.link(a, b)
    db.link(b, a)
    route = db.graph.path(a, b)
    assert [n.id for n in route] == [a.id, b.id]


def test_path_same_node(db):
    a = db.node().save()
    route = db.graph.path(a, a)
    assert [n.id for n in route] == [a.id]


def test_path_unreachable(db):
    a, b = db.node().save(), db.node().save()
    assert db.graph.path(a, b) is None


def test_subgraph_depth(db):
    a, b, c, d = (db.node().save() for _ in range(4))
    db.link(a, b)
    db.link(b, c)
    db.link(a, d)
    depth1 = {r["node"].id for r in db.graph.subgraph(a, max_depth=1)}
    assert depth1 == {a.id, b.id, d.id}
    depth2 = {r["node"].id for r in db.graph.subgraph(a, max_depth=2)}
    assert depth2 == {a.id, b.id, d.id, c.id}


def test_subgraph_link_type_filter(db):
    a, b, c = db.node().save(), db.node().save(), db.node().save()
    db.link(a, b, "tag")
    db.link(a, c, "rel")
    ids = {r["node"].id for r in db.graph.subgraph(a, max_depth=1, link_type="tag")}
    assert ids == {a.id, b.id}


def test_subgraph_cycle_terminates(db):
    a, b = db.node().save(), db.node().save()
    db.link(a, b)
    db.link(b, a)
    ids = {r["node"].id for r in db.graph.subgraph(a, max_depth=5)}
    assert ids == {a.id, b.id}