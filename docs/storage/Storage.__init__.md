# `mnemosine.storage.Storage.__init__`

**Kind:** method

## Signature

```python
Storage.__init__(self, path='mnemosine.db', blob_root=None)
```

## Documentation

Create a Storage handle (no connection is opened yet).

Call `connect` (or use the `with` statement) before any
operation. File content lives in the blob store directory while node
metadata and links live in the SQLite database.


**Args:**
- `path (str | os.PathLike)`: Path to the SQLite database file.
- Defaults to `"mnemosine.db"`.
- `blob_root (str | os.PathLike | None)`: Directory where file
- contents are stored. When omitted, defaults to a sibling
- directory named `<db-stem>.blobs` next to the database.


**Returns:**
- `Storage`: A new, disconnected Storage.


**Example:**

```python
>>> db = Storage("project.db", blob_root="data/blobs")
>>> db.connect()  # doctest: +SKIP
```
