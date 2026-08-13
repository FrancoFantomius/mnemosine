# `mnemosine.storage.Storage.embed`

**Kind:** method

## Signature

```python
Storage.embed(self, node, text=None)
```

## Documentation

Compute and store an embedding for a node.

See :func:`mnemosine.embed.embed`. Requires ``embed_fn``.


**Args:**
- `node (Node)`: The node to embed.
- `text (str | None)`: Optional text; defaults to ``node.content``.


**Returns:**
- `list of float`: The computed embedding.


**Raises:**
- `EmbeddingRequired`: If ``embed_fn`` is unset or there is no text.
- `VectorError`: If the embedding function returns an invalid vector.


**Example:**

```python
>>> db.embed_fn = lambda t: [1.0, 0.0]
>>> db.embed(doc)
[1.0, 0.0]
```
