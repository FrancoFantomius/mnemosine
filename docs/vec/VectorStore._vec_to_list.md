# `mnemosine.vec.VectorStore._vec_to_list`

**Kind:** method

## Signature

```python
VectorStore._vec_to_list(raw)
```

## Documentation

Convert a stored vector (bytes or JSON) into a Python list.

`sqlite-vec` returns raw little-endian float32 bytes; the fallback
table stores JSON text. Both are handled here.


**Args:**
- `raw (bytes | str)`: The raw stored vector.


**Returns:**
- `list of float`: The decoded vector.


**Example:**

```python
>>> VectorStore._vec_to_list(b'\x00\x00\x80?')
[1.0]
```
