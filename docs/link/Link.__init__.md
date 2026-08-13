# `mnemosine.link.Link.__init__`

**Kind:** method

## Signature

```python
Link.__init__(self, storage, source_id, target_id, link_type, metadata=None, created_at=None)
```

## Documentation

Create an in-memory Link.

Normal code should use :meth:`Link.create`,
:meth:`mnemosine.Storage.link` or :meth:`mnemosine.Node.link` instead.


**Args:**
- `storage (Storage)`: The owning storage.
- `source_id (str)`: The source node id.
- `target_id (str)`: The target node id.
- `link_type (str)`: The link type.
- `metadata (dict | None)`: Optional link attributes.
- `created_at (str | None)`: ISO-8601 timestamp; defaults to now when
- created via :meth:`Link.create`.


**Returns:**
- `Link`: The new link object.
