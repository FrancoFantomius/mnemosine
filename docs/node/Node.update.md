# `mnemosine.node.Node.update`

**Kind:** method

## Signature

```python
Node.update(self, **values)
```

## Documentation

Set several dynamic attributes at once.

Merges ``values`` into the metadata. Returns ``self`` so calls can be
chained. Persist with :meth:`save`.


**Args:**
- `**values`: Arbitrary keyword arguments stored as attributes. Note
- that ``content=...`` goes into the JSON metadata, not the
- ``content`` column - assign :attr:`content` directly for that.


**Returns:**
- `Node`: This node, for chaining.


**Example:**

```python
>>> doc.update(title="Plan", done=False).save()
```
