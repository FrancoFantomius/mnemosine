# `mnemosine.file.File._rel_path_for`

**Kind:** method

## Signature

```python
File._rel_path_for(digest: str) -> str
```

## Documentation

Compute the content-addressed blob path for a digest.


**Args:**
- `digest (str)`: A 64-char hex SHA-256 digest.


**Returns:**
- `str`: A POSIX-style relative path ``blobs/<first2>/<digest>``.


**Example:**

```python
>>> File._rel_path_for("ab" * 32)
'blobs/ab/abababababababababababababababababababababababababababababababab'
```
