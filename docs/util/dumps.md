# `mnemosine.util.dumps`

**Kind:** function

## Signature

```python
dumps(value) -> str
```

## Documentation

Serialize a Python value to a compact JSON string.

Uses `ensure_ascii=False` so non-ASCII text is kept readable, and
compact separators so the stored metadata stays small.


**Args:**
- `value (object)`: Any JSON-serializable value (dict, list, str, int, ...).


**Returns:**
- `str`: The compact JSON representation of `value`.


**Raises:**
- `TypeError`: If `value` is not JSON-serializable.


**Example:**

```python
>>> from mnemosine.util import dumps
>>> dumps({"title": "città", "n": 1})
'{"title":"città","n":1}'
```
