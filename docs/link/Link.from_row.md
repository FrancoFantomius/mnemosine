# `mnemosine.link.Link.from_row`

**Kind:** method

## Signature

```python
Link.from_row(cls, storage, row)
```

## Documentation

Build a Link from a ``node_links`` row.

Internal helper.


**Args:**
- `storage (Storage)`: The owning storage.
- `row (sqlite3.Row)`: A row from the ``node_links`` table.


**Returns:**
- `Link`: The loaded link.


**Example:**

```python
>>> row = db.conn.execute("SELECT * FROM node_links").fetchone()
>>> Link.from_row(db, row)
<Link ...>
```
