# `mnemosine.exceptions.VectorError`

**Kind:** class

## Signature

```python
class VectorError
```

## Documentation

Raised for vector-related problems.

Covers dimension mismatches, unsupported metrics, malformed vectors and
any other error produced by the vector store (native `sqlite-vec` or the
brute-force fallback).


**Example:**

```python
>>> from mnemosine import VectorError
>>> raise VectorError("dimension mismatch: stored vectors are 3d, got 2d")
Traceback (most recent call last):
...
mnemosine.exceptions.VectorError: dimension mismatch: stored vectors are 3d, got 2d
```
