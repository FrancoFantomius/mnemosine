# `mnemosine.vec.VectorStore._ensure_native`

**Kind:** method

## Signature

```python
VectorStore._ensure_native(self, dims: int, metric: str)
```

## Documentation

Create the ``nodes_vec`` virtual table and record metadata.

Fixes the table dimension/metric on first use; a later vector with a
different dimension raises. Validates the metric against
:data:`METRICS`.


**Args:**
- `dims (int)`: Embedding dimension.
- `metric (str)`: Distance metric for the ``vec0`` table.


**Returns:**
- None


**Raises:**
- `VectorError`: If ``metric`` is unsupported or the dimension
- conflicts with previously stored vectors.


**Example:**

```python
>>> db.vec._ensure_native(3, "cosine")  # doctest: +SKIP
```
