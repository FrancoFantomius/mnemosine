# `mnemosine.graph._as_id`

**Kind:** function

## Signature

```python
_as_id(obj)
```

## Documentation

Resolve a Node instance or id string to an id.


**Args:**
- `obj (Node | str)`: A node or its id.


**Returns:**
- `str`: The node id.


**Example:**

```python
>>> from mnemosine.graph import _as_id
>>> _as_id("abc")
'abc'
```
