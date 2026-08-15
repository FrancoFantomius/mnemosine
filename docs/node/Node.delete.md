# `mnemosine.node.Node.delete`

**Kind:** method

## Signature

```python
Node.delete(self)
```

## Documentation

Delete this node from the database.

Also removes its links (via `ON DELETE CASCADE`), blob metadata row
and any stored embedding. Blob files on disk are left for
`mnemosine.Storage.gc_blobs`.


**Returns:**
- None


**Example:**

```python
>>> doc.delete()
```
