# `mnemosine.vec.VectorStore._ensure_fallback_table`

**Kind:** method

## Signature

```python
VectorStore._ensure_fallback_table(self)
```

## Documentation

Create the fallback table if it does not exist.

Creates ``embedding_fallback(node_id, dims, vec)``, used when the
sqlite-vec extension is unavailable.


**Returns:**
- None


**Example:**

```python
>>> db.vec._ensure_fallback_table()  # doctest: +SKIP
```
