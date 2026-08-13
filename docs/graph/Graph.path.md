# `mnemosine.graph.Graph.path`

**Kind:** method

## Signature

```python
Graph.path(self, start, target, max_depth=100)
```

## Documentation

Find the shortest undirected path between two nodes via BFS.

Returns ``None`` when no path exists within ``max_depth``. The route
includes both endpoints, in order.


**Args:**
- `start (Node | str)`: The starting node (or id).
- `target (Node | str)`: The target node (or id).
- `max_depth (int)`: Maximum number of hops to explore.


**Returns:**
- `list of Node | None`: The shortest route from ``start`` to
- ``target`` (inclusive), or ``None`` if unreachable.


**Example:**

```python
>>> db.link(a, b); db.link(b, c)
>>> [n.id for n in db.graph.path(a, c)]
['a', 'b', 'c']
>>> db.graph.path(a, d)
None
```
