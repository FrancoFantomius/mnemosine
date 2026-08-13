# `mnemosine.graph.Graph.subgraph`

**Kind:** method

## Signature

```python
Graph.subgraph(self, node, max_depth=1, link_type=None)
```

## Documentation

Return every node reachable from ``node`` within ``max_depth`` hops.

Uses a ``WITH RECURSIVE`` CTE; cycle-safe because the recursion depth
is bounded and rows are deduplicated with ``UNION``.


**Args:**
- `node (Node | str)`: The starting node (or id).
- `max_depth (int)`: Maximum number of link hops.
- `link_type (str | None)`: Only traverse links of this type.


**Returns:**
- `list of dict`: Each item has ``node`` (Node) and ``depth`` (int),
- ordered by depth.


**Example:**

```python
>>> db.link(a, b); db.link(b, c)
>>> [(r["node"].id, r["depth"]) for r in db.graph.subgraph(a, max_depth=2)]
[('a', 0), ('b', 1), ('c', 2)]
```
