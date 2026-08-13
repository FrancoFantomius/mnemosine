# `mnemosine.node.Node.__delitem__`

**Kind:** method

## Signature

```python
Node.__delitem__(self, key)
```

## Documentation

Remove a dynamic attribute from the node's metadata.


**Args:**
- `key (str)`: The attribute name.


**Raises:**
- `KeyError`: If ``key`` is not present in the metadata.


**Example:**

```python
>>> del doc["title"]
```
