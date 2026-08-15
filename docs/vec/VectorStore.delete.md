# `mnemosine.vec.VectorStore.delete`

**Kind:** method

## Signature

```python
VectorStore.delete(self, node_id: str) -> None
```

## Documentation

Remove the embedding for a node and clear its `embedding` flag.

Touches both the native and fallback tables so the vector is removed
whichever path stored it. Does not delete the node itself.


**Args:**
- `node_id (str)`: The node id.


**Returns:**
- None


**Example:**

```python
>>> db.vec.delete(doc.id)
```
