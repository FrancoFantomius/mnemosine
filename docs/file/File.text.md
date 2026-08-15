# `mnemosine.file.File.text`

**Kind:** method

## Signature

```python
File.text(self, encoding='utf-8') -> str
```

## Documentation

Return the stored content decoded as text.


**Args:**
- `encoding (str)`: Text encoding to use. Defaults to UTF-8.


**Returns:**
- `str`: The decoded content.


**Raises:**
- `FileNotFound`: If the file has no stored content.
- `UnicodeDecodeError`: If the bytes are not valid in `encoding`.


**Example:**

```python
>>> f.write(b"hello")
>>> f.text()
'hello'
```
