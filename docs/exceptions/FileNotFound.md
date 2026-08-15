# `mnemosine.exceptions.FileNotFound`

**Kind:** class

## Signature

```python
class FileNotFound
```

## Documentation

Raised when a File has no stored content to read.

Either the file node has never had content written (`write()` not yet
called) or the underlying blob file is missing from the blob store.

Attributes:
node_id (str): The id of the file node without content.


**Example:**

```python
>>> from mnemosine import Storage, FileNotFound
>>> with Storage(":memory:") as db:
...     f = db.file("empty.txt")
...     f.save()
...     try:
...         f.read()
...     except FileNotFound:
...         print("no content yet")
no content yet
```
