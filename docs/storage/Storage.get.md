# `mnemosine.storage.Storage.get`

**Kind:** method

## Signature

```python
Storage.get(self, node_id, default=_MISSING)
```

## Documentation

Load a node (or file) by id.

Returns a `File` when the stored `kind` is `"file"`,
otherwise a `Node`.


**Args:**
- `node_id (str)`: The node id.
- `default (object)`: Value returned when the node is missing. By
- default `NodeNotFound` is raised instead.


**Returns:**
- `Node | File | object`: The loaded node/file, or `default`.


**Raises:**
- `NodeNotFound`: If the node does not exist and no `default` was
- given.


**Example:**

```python
>>> loaded = db.get(doc.id)
>>> loaded["title"]
'One'
>>> db.get("nope", default=None)
None
```
