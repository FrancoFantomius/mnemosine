# `mnemosine.migrations._base`

**Kind:** function

## Signature

```python
_base(conn)
```

## Documentation

Apply the base schema (migration 001).

Executes every statement in :data:`mnemosine.schema.BASE_SCHEMA` against
the connection. Called only when a database's ``user_version`` is below 1.


**Args:**
- `conn (sqlite3.Connection)`: An open connection to the database.


**Returns:**
- None


**Example:**

```python
>>> from mnemosine.migrations import _base
>>> import sqlite3
>>> conn = sqlite3.connect(":memory:")
>>> _base(conn)
>>> conn.execute("SELECT name FROM sqlite_master WHERE name='nodes'").fetchone()[0]
'nodes'
```
