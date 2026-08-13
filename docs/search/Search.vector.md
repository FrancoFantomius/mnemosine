# `mnemosine.search.Search.vector`

**Kind:** method

## Signature

```python
Search.vector(self, vector, top_k=10, metric='cosine')
```

## Documentation

k-NN over stored embeddings.

Delegates to :meth:`mnemosine.vec.VectorStore.knn`, which uses the
``sqlite-vec`` virtual table when available and a brute-force scan
otherwise.


**Args:**
- `vector (sequence of float)`: The query embedding.
- `top_k (int)`: Number of nearest neighbours to return.
- `metric (str)`: Distance metric: ``"cosine"`` (default), ``"l2"``
- or ``"dot"``.


**Returns:**
- `list of dict`: Each item has ``node`` (Node) and ``distance``
- (float), ordered nearest-first.


**Raises:**
- `VectorError`: If ``top_k < 1`` or the vector dimension conflicts
- with stored embeddings.


**Example:**

```python
>>> db.embed_fn = lambda t: [1.0, 0.0, 0.0]
>>> doc.add_embedding()
>>> [r["node"].id for r in db.search.vector([1.0, 0.0, 0.0], top_k=1)]
['01G...']
```
