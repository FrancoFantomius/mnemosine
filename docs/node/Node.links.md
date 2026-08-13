# `mnemosine.node.Node.links`

**Kind:** method

## Signature

```python
Node.links(self, direction='both', link_type=None)
```

## Documentation

Return the Link objects incident to this node.


**Args:**
- `direction (str)`: ``"out"`` (this node is source), ``"in"`` (this
- node is target) or ``"both"``.
- `link_type (str | None)`: Only links of this type.


**Returns:**
- `list of Link`: The matching links.


**Example:**

```python
>>> for link in doc.links(direction="out"):
...     print(link.target_id, link.link_type)
... # doctest: +SKIP
```
