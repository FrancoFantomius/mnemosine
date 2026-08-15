# `mnemosine.node.Node.metadata`

**Kind:** property

## Signature

```python
Node.metadata(self)
```

## Documentation

The dynamic attribute dictionary.

Mutating the returned dict (or replacing it) changes the node; persist
with `save`.


**Returns:**
- `dict`: A live reference to the node's metadata.


**Example:**

```python
>>> doc.metadata["title"] = "Renamed"
>>> doc.save()
```

---

## Property setter

```python
Node.metadata(self, value)
```

Replace the entire metadata dictionary.


**Args:**
- `value (dict | None)`: New metadata. `None` becomes an empty dict.


**Example:**

```python
>>> doc.metadata = {"title": "New"}
```
