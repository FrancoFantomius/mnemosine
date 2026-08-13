# `mnemosine.storage.Storage.file`

**Kind:** method

## Signature

```python
Storage.file(self, name=None, mime=None)
```

## Documentation

Create a new unsaved :class:`File`.

Binary content is written to the blob store with
:meth:`File.write`; until then the file has no content.


**Args:**
- `name (str | None)`: Logical file name or path.
- `mime (str | None)`: MIME type (stored in metadata).


**Returns:**
- `File`: A new unsaved file node.


**Example:**

```python
>>> f = db.file("report.pdf", mime="application/pdf")
>>> f.write(b"%PDF-1.4")
```
