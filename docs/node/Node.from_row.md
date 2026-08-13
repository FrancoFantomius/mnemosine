# `mnemosine.node.Node.from_row`

**Kind:** method

## Signature

```python
Node.from_row(cls, storage, row)
```

## Documentation

Build a node from a database row.

Internal helper used by :meth:`mnemosine.Storage.get`. Do not call
directly.


**Args:**
- `storage (Storage)`: The owning storage.
- `row (sqlite3.Row)`: A row from the ``nodes`` table.


**Returns:**
- `Node`: A loaded node (subclass for ``kind == "file"``).


**Example:**

```python
>>> row = db.conn.execute("SELECT * FROM nodes").fetchone()
>>> Node.from_row(db, row)
<Node ...>
```
