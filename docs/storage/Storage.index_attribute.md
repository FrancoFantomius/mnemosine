# `mnemosine.storage.Storage.index_attribute`

**Kind:** method

## Signature

```python
Storage.index_attribute(self, attr, as_type='TEXT')
```

## Documentation

Add a generated column and index for a JSON metadata attribute.

See `mnemosine.schema.index_json_attribute`. Enables fast
lookups on dynamic attributes without migrations.


**Args:**
- `attr (str)`: The metadata attribute to index.
- `as_type (str)`: SQL type: `TEXT`, `INTEGER`, `REAL` or
- `BLOB`. Defaults to `TEXT`.


**Returns:**
- `str`: The generated column name.


**Raises:**
- `ValueError`: If `as_type` is not a supported SQL type.


**Example:**

```python
>>> col = db.index_attribute("priority", as_type="INTEGER")
>>> db.conn.execute(f"SELECT count(*) FROM nodes WHERE {col} > 3").fetchone()[0]
0
```
