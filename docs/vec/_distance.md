# `mnemosine.vec._distance`

**Kind:** function

## Signature

```python
_distance(a, b, metric: str) -> float
```

## Documentation

Compute a distance between two same-length vectors.

Supports `l2` (Euclidean), `dot` (negated dot product) and
`cosine` (1 - cosine similarity; returns 1.0 if either vector has zero
magnitude).


**Args:**
- `a (sequence of float)`: First vector.
- `b (sequence of float)`: Second vector.
- `metric (str)`: `"l2"`, `"dot"` or `"cosine"`.


**Returns:**
- `float`: The distance. Lower means closer.


**Raises:**
- `VectorError`: If the vectors have different lengths.


**Example:**

```python
>>> from mnemosine.vec import _distance
>>> round(_distance([1, 0], [1, 0], "cosine"), 3)
0.0
```
