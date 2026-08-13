# `mnemosine.storage.Storage.unlink`

**Kind:** method

## Signature

```python
Storage.unlink(self, source, target, link_type='link')
```

## Documentation

Remove a link between two nodes (or ids).


**Args:**
- `source (Node | str)`: Source node or id.
- `target (Node | str)`: Target node or id.
- `link_type (str)`: The link type to remove.


**Returns:**
- None


**Example:**

```python
>>> db.unlink(doc, pdf, "attachment")
```
