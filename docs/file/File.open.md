# `mnemosine.file.File.open`

**Kind:** method

## Signature

```python
File.open(self)
```

## Documentation

Open the stored content as a binary file object.


**Returns:**
- `BinaryIO`: A file handle positioned at the start of the content.


**Raises:**
- `FileNotFound`: If this file has no stored content or the blob file
- is missing from disk.


**Example:**

```python
>>> with f.open() as fh:
...     head = fh.read(10)
```
