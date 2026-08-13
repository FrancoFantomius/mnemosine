# `mnemosine.graph.Graph.__init__`

**Kind:** method

## Signature

```python
Graph.__init__(self, storage)
```

## Documentation

Wrap a Storage and expose graph operations.

Access a ``Graph`` through ``storage.graph`` rather than constructing
it directly.


**Args:**
- `storage (Storage)`: The storage whose links are traversed.


**Returns:**
- `Graph`: A graph view over the storage.
