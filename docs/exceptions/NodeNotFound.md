# `mnemosine.exceptions.NodeNotFound`

**Kind:** class

## Signature

```python
class NodeNotFound
```

## Documentation

Raised when a node id does not exist in the database.

Thrown by :meth:`mnemosine.Storage.get` unless a ``default`` is supplied.

Attributes:
node_id (str): The id that could not be found.


**Example:**

```python
>>> from mnemosine import Storage, NodeNotFound
>>> with Storage(":memory:") as db:
...     try:
...         db.get("missing")
...     except NodeNotFound as e:
...         print(e.node_id)
missing
```
