# `mnemosine.vec.VectorStore._native_table_exists`

**Kind:** method

## Signature

```python
VectorStore._native_table_exists(self) -> bool
```

## Documentation

Return whether the `nodes_vec` virtual table has been created.

Internal guard used before touching the native table, which only
exists once a vector has been stored.


**Returns:**
- `bool`: `True` if the table exists.


**Example:**

```python
>>> db.vec._native_table_exists()
False
```
