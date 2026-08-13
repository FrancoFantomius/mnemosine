# `mnemosine.node.Node.__init__`

**Kind:** method

## Signature

```python
Node.__init__(self, storage, id=None, kind='text', path=None, content=None, metadata=None)
```

## Documentation

Create a new, unsaved node.

Constructing a node does not touch the database; call :meth:`save` to
persist it. In normal usage you do not instantiate this directly -
use :meth:`mnemosine.Storage.node` instead.


**Args:**
- `storage (Storage)`: The storage the node belongs to.
- `id (str | None)`: Explicit node id. Defaults to a fresh ULID.
- `kind (str)`: Coarse type discriminator (``"text"``, ``"doc"``,
- ``"file"``, or any custom value). Defaults to ``"text"``.
- `path (str | None)`: Optional logical name or path for the node.
- `content (str | None)`: Optional text content stored in a dedicated
- column.
- `metadata (dict | None)`: Initial dynamic attributes.


**Returns:**
- `Node`: A new unsaved node instance.


**Example:**

```python
>>> from mnemosine import Storage
>>> with Storage(":memory:") as db:
...     doc = db.node(kind="doc", path="notes/hello")
...     doc["title"] = "Hello"
...     doc.save()
...     print(doc.id, doc.kind, doc.path)
01G... doc notes/hello
```
