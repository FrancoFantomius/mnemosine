# `mnemosine.ids._encode`

**Kind:** function

## Signature

```python
_encode(value: int, bits: int) -> str
```

## Documentation

Encode an integer as Crockford base32 over a fixed number of bits.

Splits ``value`` into 5-bit groups (least significant first) and maps each
group to a character from ``_ALPHABET``. The width is ``ceil(bits / 5)``;
any bits above ``bits`` are silently ignored.


**Args:**
- `value (int)`: The non-negative integer to encode.
- `bits (int)`: The total bit width the encoding should cover.


**Returns:**
- `str`: The fixed-width Crockford base32 representation.


**Example:**

```python
>>> from mnemosine.ids import _encode
>>> _encode(26, 5)   # 26 == 11010 -> alphabet[26] == 'Q'
'Q'
```
