# `mnemosine.embed.embed`

**Kind:** function

## Signature

```python
embed(storage, node, text=None)
```

## Documentation

Compute and store an embedding for ``node``.

Uses ``storage.embed_fn`` to turn text into a vector, validates that the
result is a non-empty sequence of numbers, and stores it via
:meth:`mnemosine.vec.VectorStore.set_vector`. When ``text`` is omitted the
node's ``content`` is embedded.


**Args:**
- `storage (Storage)`: The storage whose ``embed_fn`` is used.
- `node (Node)`: The node to embed.
- `text (str | None)`: Explicit text to embed. Defaults to
- ``node.content``.


**Returns:**
- `list of float`: The computed embedding vector.


**Raises:**
- `EmbeddingRequired`: If ``storage.embed_fn`` is not set, or there is no
- text to embed.
- `VectorError`: If ``embed_fn`` returns something other than a
- non-empty sequence of numbers.


**Example:**

```python
>>> db.embed_fn = lambda text: [1.0 if "storage" in text else 0.0, 0.0]
>>> from mnemosine.embed import embed
>>> embed(db, doc)
[1.0, 0.0]
```
