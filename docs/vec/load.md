# `mnemosine.vec.load`

**Kind:** function

## Signature

```python
load(conn) -> bool
```

## Documentation

Load the sqlite-vec extension into ``conn``.

The ``sqlite_vec`` package import is attempted only once, but the
extension itself must be registered on every connection, so this should be
called for each new connection (``Storage.connect`` does this
automatically).


**Args:**
- `conn (sqlite3.Connection)`: The connection to load the extension into.


**Returns:**
- `bool`: ``True`` if the extension is now usable on ``conn``, ``False``
- if it could not be imported or loaded (the library falls back to the
- brute-force store in that case).


**Example:**

```python
>>> import sqlite3
>>> from mnemosine import vec
>>> conn = sqlite3.connect(":memory:")
>>> vec.load(conn)
True
```
