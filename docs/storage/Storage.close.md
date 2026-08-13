# `mnemosine.storage.Storage.close`

**Kind:** method

## Signature

```python
Storage.close(self)
```

## Documentation

Close the database connection.

Safe to call when already closed. After closing, call :meth:`connect`
again to reopen.


**Returns:**
- None


**Example:**

```python
>>> db.close()
```
