# `mnemosine.link.Link.source`

**Kind:** method

## Signature

```python
Link.source(self)
```

## Documentation

Load and return the source node.


**Returns:**
- `Node`: The source node object.


**Raises:**
- `NodeNotFound`: If the source node was deleted.


**Example:**

```python
>>> link.source()
<Node id='...' kind='doc'>
```
