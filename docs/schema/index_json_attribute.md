# `mnemosine.schema.index_json_attribute`

**Kind:** function

## Signature

```python
index_json_attribute(conn, attr: str, as_type: str='TEXT') -> str
```

## Documentation

Materialize a metadata JSON attribute as a generated column plus index.

Adds a ``VIRTUAL`` generated column to ``nodes`` that extracts
``metadata.attr`` (using ``json_extract``) and creates an index on it, so
``WHERE metadata->'attr' = ...`` style queries can use the index. Safe to
call repeatedly: existing columns and indexes are left untouched.


**Args:**
- `conn (sqlite3.Connection)`: An open connection to the database.
- `attr (str)`: The metadata attribute to index.
- `as_type (str)`: SQL type for the column: ``TEXT``, ``INTEGER``,
- ``REAL`` or ``BLOB``. Defaults to ``TEXT``.


**Returns:**
- `str`: The name of the generated column (``<attr>_gen``).


**Raises:**
- `ValueError`: If ``as_type`` is not one of ``TEXT``/``INTEGER``/
- ``REAL``/``BLOB``.


**Example:**

```python
>>> from mnemosine import Storage
>>> with Storage(":memory:") as db:
...     db.node(kind="doc").update(n=1).save()
...     db.node(kind="doc").update(n=2).save()
...     col = db.index_attribute("n", as_type="INTEGER")
...     db.conn.execute(f"SELECT count(*) FROM nodes WHERE {col} > 1").fetchone()[0]
1
```
