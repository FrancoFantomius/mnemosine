# `mnemosine.vec.VectorStore._metric`

**Kind:** method

## Signature

```python
VectorStore._metric(self)
```

## Documentation

Return the recorded distance metric (defaults to `"cosine"`).


**Returns:**
- `str`: The metric stored in `vec_meta`, or `"cosine"`.


**Example:**

```python
>>> db.vec._metric()
'cosine'
```
