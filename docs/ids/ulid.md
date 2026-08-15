# `mnemosine.ids.ulid`

**Kind:** function

## Signature

```python
ulid() -> str
```

## Documentation

Return a new 26-char ULID.

The first 10 characters encode the current Unix time in milliseconds
(48 bits) and the remaining 16 characters encode 80 bits of randomness
generated via the CSPRNG `secrets` module. Because the timestamp comes
first, ULIDs sort lexicographically in creation order.


**Returns:**
- `str`: A 26-character Crockford base32 ULID.


**Raises:**
- `NotImplementedError`: If the platform's `secrets`/`os.urandom`
- cannot provide cryptographic randomness.


**Example:**

```python
>>> from mnemosine.ids import ulid
>>> a, b = ulid(), ulid()
>>> len(a) == 26 and a != b
True
```
