# `mnemosine.search.Search.__init__`

**Kind:** method

## Signature

```python
Search.__init__(self, storage)
```

## Documentation

Wrap a Storage and expose search operations.

Access a ``Search`` through ``storage.search`` rather than
constructing it directly.


**Args:**
- `storage (Storage)`: The storage to search.


**Returns:**
- `Search`: A search view over the storage.
