# `mnemosine.exceptions.MnemosineError`

**Kind:** class

## Signature

```python
class MnemosineError
```

## Documentation

Base class for all mnemosine errors.

Every exception defined in this module (and any future one) subclasses
this type. Catch it to handle any library failure.


**Example:**

```python
>>> from mnemosine import Storage, MnemosineError
>>> try:
...     with Storage(":memory:"):
...         raise MnemosineError("boom")
... except MnemosineError:
...     print("caught")
caught
```
