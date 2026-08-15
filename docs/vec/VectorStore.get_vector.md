# `mnemosine.vec.VectorStore.get_vector`

**Kind:** method

## Signature

```python
VectorStore.get_vector(self, node_id: str)
```

## Documentation

Return the stored embedding for a node, or `None`.


**Args:**
- `node_id (str)`: The node id.


**Returns:**
- `list of float | None`: The embedding as a Python list, or `None`
- if the node has no stored vector.


**Example:**

```python
>>> db.vec.get_vector(doc.id)
[1.0, 0.0, 0.0]
```
