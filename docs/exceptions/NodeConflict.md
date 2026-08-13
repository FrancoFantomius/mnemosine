# `mnemosine.exceptions.NodeConflict`

**Kind:** class

## Signature

```python
class NodeConflict
```

## Documentation

Raised when a node cannot be created because one with the id already exists.

Reserved for future use by explicit-id insertion paths; base schema saves
generate fresh ULIDs and therefore never conflict.


**Example:**

```python
>>> from mnemosine import NodeConflict
>>> raise NodeConflict("duplicate id")
Traceback (most recent call last):
...
mnemosine.exceptions.NodeConflict: duplicate id
```
