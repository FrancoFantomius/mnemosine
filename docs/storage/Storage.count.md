# `mnemosine.storage.Storage.count`

**Kind:** method

## Signature

```python
Storage.count(self, kind=None) -> int
```

## Documentation

Count nodes, optionally of a single kind.


**Args:**
- `kind (str | None)`: Count only this kind when given.


**Returns:**
- `int`: The number of matching nodes.


**Example:**

```python
>>> db.count(kind="doc")
3
```
