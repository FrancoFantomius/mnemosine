# `mnemosine.node.Node.__contains__`

**Kind:** method

## Signature

```python
Node.__contains__(self, key)
```

## Documentation

Return whether the metadata holds ``key``.


**Args:**
- `key (str)`: The attribute name.


**Returns:**
- `bool`: ``True`` if ``key`` is present in the metadata.


**Example:**

```python
>>> "title" in doc
True
```
