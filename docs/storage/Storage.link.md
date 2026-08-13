# `mnemosine.storage.Storage.link`

**Kind:** method

## Signature

```python
Storage.link(self, source, target, link_type='link', metadata=None)
```

## Documentation

Create a link between two nodes (or ids).

Idempotent: linking the same pair with the same type returns the
existing link. See :meth:`Link.create`.


**Args:**
- `source (Node | str)`: Source node or id.
- `target (Node | str)`: Target node or id.
- `link_type (str)`: The link type. Defaults to ``"link"``.
- `metadata (dict | None)`: Optional JSON-serializable attributes.


**Returns:**
- `Link`: The created (or existing) link.


**Example:**

```python
>>> db.link(doc, pdf, "attachment", {"label": "v1"})
```
