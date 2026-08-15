# `mnemosine.node.Node.save`

**Kind:** method

## Signature

```python
Node.save(self)
```

## Documentation

Persist this node to the database.

Inserts a new row on first call, or updates the existing row on
subsequent calls. Wrapped in a transaction; when called inside an
outer `mnemosine.Storage.transaction`, it joins that
transaction instead.


**Returns:**
- `Node`: This node, for chaining.


**Raises:**
- `sqlite3.Error`: If the database write fails.


**Example:**

```python
>>> doc = db.node(kind="doc")
>>> doc["title"] = "Hello"
>>> doc.save()          # doctest: +SKIP
<Node id='01G...' kind='doc'>
```
