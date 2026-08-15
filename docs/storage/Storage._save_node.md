# `mnemosine.storage.Storage._save_node`

**Kind:** method

## Signature

```python
Storage._save_node(self, node)
```

## Documentation

Persist a node inside a transaction.

Internal: called by `Node.save`.


**Args:**
- `node (Node)`: The node to save.


**Returns:**
- `Node`: The saved node.


**Example:**

```python
>>> db._save_node(doc)
```
