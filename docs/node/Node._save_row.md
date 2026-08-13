# `mnemosine.node.Node._save_row`

**Kind:** method

## Signature

```python
Node._save_row(self, conn)
```

## Documentation

Insert or update this node's row in ``conn``.

Internal: called from within a transaction by ``storage._save_node``.


**Args:**
- `conn (sqlite3.Connection)`: The connection to write through.


**Returns:**
- None


**Example:**

```python
>>> db._save_node(doc)  # indirect usage
```
