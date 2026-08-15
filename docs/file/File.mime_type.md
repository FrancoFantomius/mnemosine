# `mnemosine.file.File.mime_type`

**Kind:** property

## Signature

```python
File.mime_type(self)
```

## Documentation

The MIME type of this file.


**Returns:**
- `str | None`: The `"mime"` metadata value, if set.


**Example:**

```python
>>> f = db.file("a.png", mime="image/png")
>>> f.mime_type
'image/png'
```
