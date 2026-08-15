# `mnemosine.file.File.write_stream`

**Kind:** method

## Signature

```python
File.write_stream(self, fileobj, chunk_size: int=1 << 16) -> str
```

## Documentation

Stream content from a binary file object into the blob store.

Reads `fileobj` in chunks of `chunk_size` bytes, hashing as it
goes, so arbitrarily large files never fully load into memory. The
data is written to a temp file first and atomically renamed to its
final content-addressed path.


**Args:**
- `fileobj (BinaryIO)`: Any object exposing `read(n) -> bytes`.
- `chunk_size (int)`: Read chunk size in bytes (default 64 KiB).


**Returns:**
- `str`: The SHA-256 digest of the streamed content.


**Raises:**
- `BlobStoreError`: If writing to the blob store fails.


**Example:**

```python
>>> import io
>>> with open("big.bin", "rb") as fh:  # doctest: +SKIP
...     digest = file.write_stream(fh)
```
