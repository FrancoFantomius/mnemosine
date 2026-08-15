# `mnemosine.exceptions.EmbeddingRequired`

**Kind:** class

## Signature

```python
class EmbeddingRequired
```

## Documentation

Raised when an embedding is requested but cannot be produced.

Two situations: no `embed_fn` has been configured on the `Storage`, or
the node has no text content to embed.


**Example:**

```python
>>> from mnemosine import Storage, EmbeddingRequired
>>> with Storage(":memory:") as db:
...     doc = db.node(kind="doc")
...     doc.save()
...     try:
...         doc.add_embedding()
...     except EmbeddingRequired:
...         print("set storage.embed_fn first")
set storage.embed_fn first
```
