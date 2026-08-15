# `mnemosine.vec.VectorStore.__init__`

**Kind:** method

## Signature

```python
VectorStore.__init__(self, storage)
```

## Documentation

Wrap a Storage and expose vector operations.

Access a `VectorStore` through `storage.vec` rather than
constructing it directly.


**Args:**
- `storage (Storage)`: The owning storage.


**Returns:**
- `VectorStore`: A vector store view over the storage.
