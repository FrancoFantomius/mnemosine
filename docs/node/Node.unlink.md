# `mnemosine.node.Node.unlink`

**Kind:** method

## Signature

```python
Node.unlink(self, target, link_type='link')
```

## Documentation

Remove a link between this node and `target`.


**Args:**
- `target (Node | str)`: The target node, or its id.
- `link_type (str)`: The link type to remove.


**Returns:**
- None


**Example:**

```python
>>> doc.unlink(attachment, link_type="attachment")
```
