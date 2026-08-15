# `mnemosine.file.File._persist`

**Kind:** method

## Signature

```python
File._persist(self)
```

## Documentation

Write the node row and blob metadata row in one transaction.

Called after content is stored on disk. Inserts or updates both the
`nodes` row (via `_save_row`) and the `blobs` row.


**Returns:**
- None


**Example:**

```python
>>> f.write(b"x")  # triggers _persist internally
```
