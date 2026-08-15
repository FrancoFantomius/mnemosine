# `mnemosine.exceptions.LinkExists`

**Kind:** class

## Signature

```python
class LinkExists
```

## Documentation

Raised when a duplicate link would be created.

The base schema treats `(source_id, target_id, link_type)` as a primary
key. `mnemosine.Link.create` is idempotent and returns the existing
link instead of raising; this exception remains for callers that pass
`INSERT`-style semantics.


**Example:**

```python
>>> from mnemosine import LinkExists
>>> raise LinkExists("link already present")
Traceback (most recent call last):
...
mnemosine.exceptions.LinkExists: link already present
```
