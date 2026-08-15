# `mnemosine.storage.Storage.exists`

**Kind:** method

## Signature

```python
Storage.exists(self, node_id) -> bool
```

## Documentation

Check whether a node id exists.


**Args:**
- `node_id (str)`: The node id.


**Returns:**
- `bool`: `True` if a node with that id exists.


**Example:**

```python
>>> db.exists(doc.id)
True
```
