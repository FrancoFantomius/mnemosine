# `mnemosine.graph.Graph.reachable`

**Kind:** method

## Signature

```python
Graph.reachable(self, node, max_depth=100)
```

## Documentation

Return all nodes reachable from ``node`` (alias of ``subgraph``).


**Args:**
- `node (Node | str)`: The starting node (or id).
- `max_depth (int)`: Maximum hops. Defaults to 100.


**Returns:**
- `list of dict`: The same shape as :meth:`subgraph`.


**Example:**

```python
>>> db.graph.reachable(a, max_depth=10)
[{'node': <Node ...>, 'depth': 0}, ...]
```
