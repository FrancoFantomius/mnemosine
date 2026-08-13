# `mnemosine.node.Node.__eq__`

**Kind:** method

## Signature

```python
Node.__eq__(self, other)
```

## Documentation

Two nodes are equal when they share the same id.


**Args:**
- `other (object)`: Any object.


**Returns:**
- `bool`: ``True`` if ``other`` is a Node with the same id.


**Example:**

```python
>>> doc == db.get(doc.id)
True
```
