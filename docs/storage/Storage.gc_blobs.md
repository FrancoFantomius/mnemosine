# `mnemosine.storage.Storage.gc_blobs`

**Kind:** method

## Signature

```python
Storage.gc_blobs(self) -> int
```

## Documentation

Delete blob files no longer referenced by any node.

Walks the blob store, removes every file whose relative path is not
referenced by the `blobs` table (and is not a temp file), then prunes
empty directories. Return the number of files removed.


**Returns:**
- `int`: Number of blob files deleted.


**Example:**

```python
>>> removed = db.gc_blobs()
>>> print(f"removed {removed} orphaned blobs")
removed 0 orphaned blobs
```
