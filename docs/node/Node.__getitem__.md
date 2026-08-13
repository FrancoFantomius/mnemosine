# `mnemosine.node.Node.__getitem__`

**Kind:** method

## Signature

```python
Node.__getitem__(self, key)
```

## Documentation

Read a dynamic attribute from the node's metadata.


**Args:**
- `key (str)`: The attribute name.


**Returns:**
- `object`: The stored value.


**Raises:**
- `KeyError`: If ``key`` is not present in the metadata.


**Example:**

```python
>>> doc["title"]
'Hello'
```
