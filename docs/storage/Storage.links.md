# `mnemosine.storage.Storage.links`

**Kind:** method

## Signature

```python
Storage.links(self, source=None, target=None, link_type=None, limit=1000)
```

## Documentation

Query links by endpoint and/or type.

Any combination of filters may be given; omitted filters are
unrestricted.


**Args:**
- `source (Node | str | None)`: Only links with this source.
- `target (Node | str | None)`: Only links with this target.
- `link_type (str | None)`: Only links of this type.
- `limit (int)`: Maximum rows. Defaults to 1000.


**Returns:**
- `list of Link`: The matching links.


**Example:**

```python
>>> outgoing = db.links(source=doc.id)
>>> tagged = db.links(link_type="tag", limit=50)
```
