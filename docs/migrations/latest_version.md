# `mnemosine.migrations.latest_version`

**Kind:** function

## Signature

```python
latest_version() -> int
```

## Documentation

Return the newest schema version known to the library.

The version is the first element of the last entry in
:data:`MIGRATIONS`. A freshly connected database is migrated up to this
value.


**Returns:**
- `int`: The latest migration version.


**Example:**

```python
>>> from mnemosine.migrations import latest_version
>>> latest_version()
1
```
