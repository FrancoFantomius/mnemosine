# `mnemosine.node.Node.link`

**Kind:** method

## Signature

```python
Node.link(self, target, link_type='link', metadata=None)
```

## Documentation

Create a link from this node to ``target``.

Convenience wrapper around :meth:`mnemosine.Storage.link`. Idempotent:
re-linking the same pair and type returns the existing link.


**Args:**
- `target (Node | str)`: The target node, or its id.
- `link_type (str)`: The link type. Defaults to ``"link"``.
- `metadata (dict | None)`: Arbitrary JSON-serializable link data.


**Returns:**
- `Link`: The created (or existing) link.


**Example:**

```python
>>> doc.link(attachment, link_type="attachment", metadata={"v": 1})
<Link ...>
```
