# `mnemosine.graph.Graph.neighbors`

**Kind:** method

## Signature

```python
Graph.neighbors(self, node, link_type=None, direction='both')
```

## Documentation

Return the nodes directly connected to ``node``.


**Args:**
- `node (Node | str)`: The node (or id) to inspect.
- `link_type (str | None)`: Only follow links of this type.
- `direction (str)`: ``"out"`` (node is the link source), ``"in"``
- (node is the link target) or ``"both"``.


**Returns:**
- `list of dict`: Each item contains ``node`` (Node), ``link_type``
- (str) and ``metadata`` (dict).


**Raises:**
- `ValueError`: If ``direction`` is not ``"out"``, ``"in"`` or
- ``"both"``.


**Example:**

```python
>>> db.link(a, b, "friend")
>>> db.link(c, a, "parent")
>>> [n["node"].id for n in db.graph.neighbors(a, direction="both")]
['b', 'c']
```
