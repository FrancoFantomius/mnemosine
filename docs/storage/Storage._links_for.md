# `mnemosine.storage.Storage._links_for`

**Kind:** method

## Signature

```python
Storage._links_for(self, node_id, direction='both', link_type=None)
```

## Documentation

Return links incident to a node in a given direction.

Internal: called by :meth:`Node.links`.


**Args:**
- `node_id (str)`: The node id.
- `direction (str)`: ``"out"``, ``"in"`` or ``"both"``.
- `link_type (str | None)`: Optional type filter.


**Returns:**
- `list of Link`: The matching links.


**Example:**

```python
>>> db._links_for(doc.id, direction="out")
```
