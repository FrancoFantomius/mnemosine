# `mnemosine.util.utcnow`

**Kind:** function

## Signature

```python
utcnow() -> str
```

## Documentation

Return the current UTC time as an ISO-8601 string.

Seconds precision, e.g. `2026-08-13T12:34:56+00:00`. Used as the
`created_at` / `updated_at` values on nodes and links.


**Returns:**
- `str`: The current UTC time formatted as ISO-8601 with seconds precision.


**Example:**

```python
>>> from mnemosine.util import utcnow
>>> utcnow()
'2026-08-13T12:34:56+00:00'
```
