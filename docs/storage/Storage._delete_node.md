# `mnemosine.storage.Storage._delete_node`

**Kind:** method

## Signature

```python
Storage._delete_node(self, node_id)
```

## Documentation

Delete a node and its dependent data inside a transaction.

Internal: called by :meth:`Node.delete`. Removes the embedding, then
the node row (links and blob row cascade via foreign keys).


**Args:**
- `node_id (str)`: The node id.


**Returns:**
- None


**Example:**

```python
>>> db._delete_node(doc.id)
```
