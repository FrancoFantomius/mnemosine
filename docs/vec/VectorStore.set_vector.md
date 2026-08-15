# `mnemosine.vec.VectorStore.set_vector`

**Kind:** method

## Signature

```python
VectorStore.set_vector(self, node_id: str, vector, metric: str='cosine') -> None
```

## Documentation

Store (or replace) the embedding for a node.

On the native path the vector is upserted into `nodes_vec` (delete +
insert); on the fallback path it is upserted into
`embedding_fallback`. Also flips the node's `embedding` flag to 1.


**Args:**
- `node_id (str)`: The node id.
- `vector (sequence of float)`: The embedding vector. Must be
- non-empty and match the recorded dimension.
- `metric (str)`: Distance metric (native path only). Defaults to
- `"cosine"`.


**Returns:**
- None


**Raises:**
- `VectorError`: If `vector` is empty/not a sequence, the metric is
- unsupported, or the dimension conflicts.


**Example:**

```python
>>> db.vec.set_vector(doc.id, [1.0, 0.0, 0.0])
```
