# `mnemosine.node.Node.neighbors`

**Kind:** method

## Signature

```python
Node.neighbors(self, link_type=None, direction='both')
```

## Documentation

Return the nodes directly connected to this node.

Delegates to `mnemosine.Graph.neighbors`.


**Args:**
- `link_type (str | None)`: Only consider links of this type.
- `direction (str)`: `"out"`, `"in"` or `"both"`.


**Returns:**
- `list of dict`: Each item has `node` (a Node), `link_type`
- (str) and `metadata` (dict).


**Example:**

```python
>>> for item in doc.neighbors(link_type="attachment"):
...     print(item["node"].id, item["link_type"])
... # doctest: +SKIP
```
