# `mnemosine.schema._json_path_key`

**Kind:** function

## Signature

```python
_json_path_key(key: str) -> str
```

## Documentation

Build a JSON path expression for a metadata key.

Simple identifiers become ``$.key``; keys with spaces or special
characters become the quoted form ``$."my key"`` with ``"`` and ``\``
escaped, which ``json_extract`` understands.


**Args:**
- `key (str)`: The JSON object key.


**Returns:**
- `str`: A path expression usable by ``json_extract(metadata, <path>)``.


**Example:**

```python
>>> from mnemosine.schema import _json_path_key
>>> _json_path_key("title")
'$.title'
>>> _json_path_key("my key")
'$."my key"'
```
