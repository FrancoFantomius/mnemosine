# `mnemosine.node.Node.updated_at`

**Kind:** property

## Signature

```python
Node.updated_at(self)
```

## Documentation

Last modification timestamp (ISO-8601 UTC).

Bumped on every `save`.


**Returns:**
- `str | None`: The last update timestamp, or `None` before the
- first save.


**Example:**

```python
>>> doc.save()
>>> doc.updated_at
'2026-08-13T12:34:56+00:00'
```
