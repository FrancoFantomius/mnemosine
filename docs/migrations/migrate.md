# `mnemosine.migrations.migrate`

**Kind:** function

## Signature

```python
migrate(conn, target: int | None=None)
```

## Documentation

Apply pending migrations to `conn`.

Reads `PRAGMA user_version`, then runs each migration whose version is
greater than the stored version (and, if given, not greater than
`target`). Each migration runs inside its own transaction so a failure
rolls back cleanly; the version is bumped only after the migration body
succeeds. Idempotent: calling again after a successful run is a no-op.


**Args:**
- `conn (sqlite3.Connection)`: An open connection to the database.
- `target (int | None)`: Optional upper bound version. Migrations above
- this value are skipped. `None` means "migrate to the latest".


**Returns:**
- `int`: The schema version that was stored before migrating (the
- `current` value).


**Raises:**
- `sqlite3.Error`: If any migration statement fails; the failed
- migration's transaction is rolled back first.


**Example:**

```python
>>> from mnemosine.migrations import migrate, latest_version
>>> import sqlite3
>>> conn = sqlite3.connect(":memory:")
>>> migrate(conn)
0
>>> conn.execute("PRAGMA user_version").fetchone()[0] == latest_version()
True
```
