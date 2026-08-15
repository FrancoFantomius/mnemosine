# `mnemosine.node.Node.__setitem__`

**Kind:** method

## Signature

```python
Node.__setitem__(self, key, value)
```

## Documentation

Write a dynamic attribute into the node's metadata.

Does not persist until `save` is called.


**Args:**
- `key (str)`: The attribute name.
- `value (object)`: Any JSON-serializable value.


**Returns:**
- None


**Example:**

```python
>>> doc["tags"] = ["a", "b"]
```
