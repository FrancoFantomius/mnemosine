# `mnemosine.vec.VectorStore.knn`

**Kind:** method

## Signature

```python
VectorStore.knn(self, vector, top_k: int=10, metric: str='cosine')
```

## Documentation

Return the ``top_k`` nearest embeddings to ``vector``.

Native path: ``vec0`` k-NN query returning ``(node_id, distance)``.
Fallback path: brute-force scan with :func:`_distance`. Result items
are ordered nearest-first.


**Args:**
- `vector (sequence of float)`: The query embedding.
- `top_k (int)`: Number of results. Defaults to 10.
- `metric (str)`: ``"cosine"`` (default), ``"l2"`` or ``"dot"``.


**Returns:**
- `list of dict`: Each item has ``node_id`` (str) and ``distance``
- (float). Empty when no embeddings are stored.


**Raises:**
- `VectorError`: If ``top_k < 1`` or the vector dimension conflicts.


**Example:**

```python
>>> db.vec.knn([1.0, 0.0, 0.0], top_k=2)
[{'node_id': '01G...', 'distance': 0.0}, ...]
```
