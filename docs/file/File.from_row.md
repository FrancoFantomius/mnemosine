# `mnemosine.file.File.from_row`

**Kind:** method

## Signature

```python
File.from_row(cls, storage, row)
```

## Documentation

Build a File from a database row, loading its blob metadata.

Internal helper used by `mnemosine.Storage.get`.


**Args:**
- `storage (Storage)`: The owning storage.
- `row (sqlite3.Row)`: A row from the `nodes` table.


**Returns:**
- `File`: A loaded file node.


**Example:**

```python
>>> row = db.conn.execute("SELECT * FROM nodes").fetchone()
>>> File.from_row(db, row)
<File ...>
```
