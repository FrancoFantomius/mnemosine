# `mnemosine.storage.Storage.list_nodes`

**Kind:** method

## Signature

```python
Storage.list_nodes(self, kind=None, limit=1000, offset=0)
```

## Documentation

List nodes, newest-updated first.


**Args:**
- `kind (str | None)`: Only return nodes of this kind.
- `limit (int)`: Maximum number of rows. Defaults to 1000.
- `offset (int)`: Row offset for pagination.


**Returns:**
- `list of Node`: The loaded nodes.


**Example:**

```python
>>> nodes = db.list_nodes(kind="doc", limit=10)
```
