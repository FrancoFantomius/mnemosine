# `mnemosine.node.Node.add_embedding`

**Kind:** method

## Signature

```python
Node.add_embedding(self, text=None)
```

## Documentation

Embed this node and store the vector.

Requires ``storage.embed_fn`` to be set. When ``text`` is omitted the
node's ``content`` is used.


**Args:**
- `text (str | None)`: Text to embed. Defaults to ``self.content``.


**Returns:**
- `list of float`: The computed embedding vector.


**Raises:**
- `EmbeddingRequired`: If no ``embed_fn`` is configured or there is
- no text to embed.
- `VectorError`: If the embedding function returns an invalid vector.


**Example:**

```python
>>> db.embed_fn = lambda t: [1.0, 0.0]  # any embedder
>>> doc.add_embedding()
[1.0, 0.0]
```
