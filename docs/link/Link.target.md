# `mnemosine.link.Link.target`

**Kind:** method

## Signature

```python
Link.target(self)
```

## Documentation

Load and return the target node.


**Returns:**
- `Node`: The target node object.


**Raises:**
- `NodeNotFound`: If the target node was deleted.


**Example:**

```python
>>> link.target()
<Node id='...' kind='doc'>
```
