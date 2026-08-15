# `mnemosine.file.File.size_bytes`

**Kind:** property

## Signature

```python
File.size_bytes(self)
```

## Documentation

Size of the stored content in bytes, or `None`.


**Returns:**
- `int | None`: The content size after `write`.


**Example:**

```python
>>> f.write(b"hello")
>>> f.size_bytes
5
```
