# `mnemosine.node.Node.refresh`

**Kind:** method

## Signature

```python
Node.refresh(self)
```

## Documentation

Reload the node's fields from the database.

Discards local, unsaved changes and re-reads `path`, `content`,
metadata and timestamps.


**Returns:**
- `Node`: This node, with fresh values.


**Raises:**
- `NodeNotFound`: If the node no longer exists.


**Example:**

```python
>>> doc["title"] = "unsaved change"
>>> doc.refresh()
>>> doc.get("title")
'Saved value'
```
