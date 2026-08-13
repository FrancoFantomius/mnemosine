# `mnemosine.file.File.__init__`

**Kind:** method

## Signature

```python
File.__init__(self, storage, name=None, mime=None, id=None, content=None, metadata=None)
```

## Documentation

Create a new, unsaved file node.

The node row is only persisted when content is written or :meth:`save`
is called explicitly. Use :meth:`mnemosine.Storage.file` in normal
code.


**Args:**
- `storage (Storage)`: The owning storage.
- `name (str | None)`: Logical file name or path (stored in
- ``node.path``).
- `mime (str | None)`: MIME type, stored under the ``"mime"``
- metadata key.
- `id (str | None)`: Explicit node id; defaults to a fresh ULID.
- `content (bytes | str | None)`: Initial content; ignored in favour
- of the blob store once :meth:`write` is used.
- `metadata (dict | None)`: Extra dynamic attributes.


**Returns:**
- `File`: A new unsaved file node.


**Example:**

```python
>>> from mnemosine import Storage
>>> with Storage(":memory:") as db:
...     f = db.file("report.pdf", mime="application/pdf")
...     print(f.path, f.kind, f.mime_type)
report.pdf file application/pdf
```
