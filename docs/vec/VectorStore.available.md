# `mnemosine.vec.VectorStore.available`

**Kind:** property

## Signature

```python
VectorStore.available(self) -> bool
```

## Documentation

Whether the native sqlite-vec extension is loaded.


**Returns:**
- `bool`: `True` when k-NN runs on the `vec0` virtual table,
- `False` when the brute-force fallback is used.


**Example:**

```python
>>> db.vec.available
True
```
