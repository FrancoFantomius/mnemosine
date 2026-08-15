# `mnemosine.search.Search.text`

**Kind:** method

## Signature

```python
Search.text(self, query, kind=None, limit=100, fields=('content', 'path', 'metadata'))
```

## Documentation

Find nodes whose text fields contain `query` literally.

Uses SQL `LIKE` with `%`/`_` escaped, so the query is matched
literally rather than as a wildcard. Matches are combined with `OR`
across the requested fields.


**Args:**
- `query (str)`: The substring to search for.
- `kind (str | None)`: Only return nodes of this kind.
- `limit (int)`: Maximum number of results. Defaults to 100.
- `fields (tuple of str)`: Columns to search: `"content"`,
- `"path"` and/or `"metadata"`.


**Returns:**
- `list of Node`: The matching nodes, newest first (unsorted).


**Raises:**
- `ValueError`: If `fields` contains an unknown column.


**Example:**

```python
>>> db.node(kind="doc").update(title="Project Plan").save()
>>> [n["title"] for n in db.search.text("Plan")]
['Project Plan']
```
