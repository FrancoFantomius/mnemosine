# `mnemosine.exceptions.BlobStoreError`

**Kind:** class

## Signature

```python
class BlobStoreError
```

## Documentation

Raised when the on-disk blob store fails (I/O, permissions, corruption).

Reserved for blob-store-level failures such as an unwritable `blob_root`
or an unreadable blob file.


**Example:**

```python
>>> from mnemosine import BlobStoreError
>>> raise BlobStoreError("blob store is unwritable")
Traceback (most recent call last):
...
mnemosine.exceptions.BlobStoreError: blob store is unwritable
```
