# `mnemosine.graph.Graph._neighbor_ids`

**Kind:** method

## Signature

```python
Graph._neighbor_ids(self, node_id, link_type=None)
```

## Documentation

Return the ids of nodes directly connected to `node_id`.

Internal BFS helper; works in both link directions.


**Args:**
- `node_id (str)`: The node id.
- `link_type (str | None)`: Optional type filter.


**Returns:**
- `list of str`: Connected node ids (deduplicated).


**Example:**

```python
>>> db.graph._neighbor_ids(a.id)
['b', 'c']
```
