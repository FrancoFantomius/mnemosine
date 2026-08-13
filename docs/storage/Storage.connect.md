# `mnemosine.storage.Storage.connect`

**Kind:** method

## Signature

```python
Storage.connect(self)
```

## Documentation

Open the database connection and prepare the schema.

Creates the database file and blob_root directory if missing, enables
``foreign_keys`` and ``WAL``, sets a busy timeout, tries to load the
sqlite-vec extension, and runs any pending migrations. Idempotent: a
second call returns without doing anything.


**Returns:**
- `Storage`: This storage, now connected.


**Raises:**
- `sqlite3.Error`: If the database cannot be opened or migrated.


**Example:**

```python
>>> db = Storage("project.db")
>>> db.connected
False
>>> db.connect()
>>> db.connected
True
```
