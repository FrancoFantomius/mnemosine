# `mnemosine.file.File.write`

**Kind:** method

## Signature

```python
File.write(self, data: bytes) -> str
```

## Documentation

Store bytes (or text) as this file's content.

Convenience wrapper around :meth:`write_stream`. Strings are encoded
as UTF-8. The bytes are streamed to a temporary file, hashed, then
atomically moved to their content-addressed location. Replaces any
previous content.


**Args:**
- `data (bytes | str)`: The content to store.


**Returns:**
- `str`: The SHA-256 digest of the content.


**Raises:**
- `BlobStoreError`: If writing to the blob store fails.


**Example:**

```python
>>> digest = f.write(b"%PDF-1.4 fake")
>>> len(digest) == 64
True
```
