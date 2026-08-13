# `mnemosine.file.File.read`

**Kind:** method

## Signature

```python
File.read(self) -> bytes
```

## Documentation

Return the entire stored content as bytes.


**Returns:**
- `bytes`: The full content.


**Raises:**
- `FileNotFound`: If the file has no stored content.


**Example:**

```python
>>> f.write(b"hello world")
>>> f.read()
b'hello world'
```
