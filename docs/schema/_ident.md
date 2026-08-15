# `mnemosine.schema._ident`

**Kind:** function

## Signature

```python
_ident(name: str) -> str
```

## Documentation

Derive a safe SQL identifier from an arbitrary metadata attribute name.

Replaces every character outside `[A-Za-z0-9_]` with an underscore and
prefixes the result with `_` when it would start with a digit.


**Args:**
- `name (str)`: The raw attribute name (e.g. `"my attr"`).


**Returns:**
- `str`: A valid SQL identifier.


**Raises:**
- `ValueError`: If `name` contains no usable characters at all.


**Example:**

```python
>>> from mnemosine.schema import _ident
>>> _ident("my attr")
'my_attr'
```
