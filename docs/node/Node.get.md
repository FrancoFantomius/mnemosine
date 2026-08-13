# `mnemosine.node.Node.get`

**Kind:** method

## Signature

```python
Node.get(self, key, default=None)
```

## Documentation

Read a dynamic attribute without raising when missing.


**Args:**
- `key (str)`: The attribute name.
- `default (object)`: Value returned when ``key`` is absent. Defaults
- to ``None``.


**Returns:**
- `object`: The stored value or ``default``.


**Example:**

```python
>>> doc.get("title", "untitled")
'Hello'
>>> doc.get("missing", "untitled")
'untitled'
```
