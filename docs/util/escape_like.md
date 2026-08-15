# `mnemosine.util.escape_like`

**Kind:** function

## Signature

```python
escape_like(term: str) -> str
```

## Documentation

Escape `LIKE` wildcards so user input matches literally.

SQL's `LIKE` treats `%` and `_` as wildcards and `\` as the
escape character. This function escapes all three so a query such as
`"100%"` matches the literal text `100%` instead of everything
starting with `100`. The SQL must use `ESCAPE '\'`.


**Args:**
- `term (str)`: The raw user-supplied search term.


**Returns:**
- `str`: The same term with `\`, `%` and `_` escaped.


**Example:**

```python
>>> from mnemosine.util import escape_like
>>> escape_like("100%_done")
'100\\%\\_done'
```
