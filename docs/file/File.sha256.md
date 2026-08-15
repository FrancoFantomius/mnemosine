# `mnemosine.file.File.sha256`

**Kind:** property

## Signature

```python
File.sha256(self)
```

## Documentation

Hex SHA-256 digest of the stored content, or `None`.

Populated after `write` (or when the node is loaded from the
database and has content).


**Returns:**
- `str | None`: The 64-char lowercase digest.


**Example:**

```python
>>> f.write(b"hello")
'2cf24dba...'
>>> f.sha256
'2cf24dba...'
```
