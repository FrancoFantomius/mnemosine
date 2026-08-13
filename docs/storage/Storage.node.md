# `mnemosine.storage.Storage.node`

**Kind:** method

## Signature

```python
Storage.node(self, kind='text', path=None, metadata=None)
```

## Documentation

Create a new unsaved :class:`Node`.

Does not write to the database until :meth:`Node.save` is called, so
attributes can be set first.


**Args:**
- `kind (str)`: The node kind. Defaults to ``"text"``.
- `path (str | None)`: Optional logical name or path.
- `metadata (dict | None)`: Initial dynamic attributes.


**Returns:**
- `Node`: A new unsaved node.


**Example:**

```python
>>> doc = db.node(kind="doc", path="notes/one")
>>> doc["title"] = "One"
>>> doc.save()
```
