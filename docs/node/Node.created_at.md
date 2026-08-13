# `mnemosine.node.Node.created_at`

**Kind:** property

## Signature

```python
Node.created_at(self)
```

## Documentation

Creation timestamp (ISO-8601 UTC), ``None`` until saved.


**Returns:**
- `str | None`: The creation timestamp after the first :meth:`save`.


**Example:**

```python
>>> doc.save()
>>> doc.created_at
'2026-08-13T12:34:56+00:00'
```
