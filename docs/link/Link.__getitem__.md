# `mnemosine.link.Link.__getitem__`

**Kind:** method

## Signature

```python
Link.__getitem__(self, key)
```

## Documentation

Read a link attribute.


**Args:**
- `key (str)`: The attribute name.


**Returns:**
- `object`: The stored value.


**Raises:**
- `KeyError`: If ``key`` is absent.


**Example:**

```python
>>> link["label"]
'cites'
```
