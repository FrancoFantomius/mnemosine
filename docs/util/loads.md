# `mnemosine.util.loads`

**Kind:** function

## Signature

```python
loads(text)
```

## Documentation

Parse a JSON string back into a Python value.

Empty or `None` input is treated as an empty mapping, which is the
convention used for the `metadata` columns.


**Args:**
- `text (str | None)`: The JSON string to parse.


**Returns:**
- `object`: The decoded value; an empty `dict` when `text` is empty
- or `None`.


**Raises:**
- `json.JSONDecodeError`: If `text` is not valid JSON.


**Example:**

```python
>>> from mnemosine.util import loads
>>> loads('{"a": 1}')
{'a': 1}
>>> loads(None)
{}
```
