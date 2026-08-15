# `mnemosine.link.Link.create`

**Kind:** method

## Signature

```python
Link.create(cls, storage, source, target, link_type='link', metadata=None)
```

## Documentation

Create and persist a link.

Idempotent: if a link with the same source, target and type already
exists, the existing link is returned instead of raising a duplicate
key error. Wrapped in a transaction.


**Args:**
- `storage (Storage)`: The owning storage.
- `source (Node | str)`: Source node or id.
- `target (Node | str)`: Target node or id.
- `link_type (str)`: The link type. Defaults to `"link"`.
- `metadata (dict | None)`: Optional JSON-serializable attributes.


**Returns:**
- `Link`: The created (or pre-existing) link.


**Raises:**
- `sqlite3.IntegrityError`: If either endpoint does not exist and
- foreign keys are enforced.


**Example:**

```python
>>> link = Link.create(db, a, b, "relation", {"label": "cites"})
>>> print(link.source_id, "->", link.target_id)
... # doctest: +SKIP
```
