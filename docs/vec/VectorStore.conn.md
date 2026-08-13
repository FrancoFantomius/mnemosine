# `mnemosine.vec.VectorStore.conn`

**Kind:** property

## Signature

```python
VectorStore.conn(self)
```

## Documentation

The underlying database connection.


**Returns:**
- `sqlite3.Connection`: The connection owned by the storage.


**Example:**

```python
>>> db.vec.conn  # doctest: +SKIP
<sqlite3.Connection object at 0x...>
```
