# `mnemosine.storage.Storage.transaction`

**Kind:** method

## Signature

```python
Storage.transaction(self)
```

## Documentation

Run a block of operations inside a single SQLite transaction.

Starts an explicit `BEGIN` when it is the outermost transaction;
nested calls join the existing transaction. Commits on success and
rolls back on any exception (re-raising it).


**Yields:**
- `Storage`: This storage, so the block can use `db.transaction()`
- or just `db`.


**Raises:**
- `BaseException`: Any exception raised inside the block is re-raised
- after rollback.


**Example:**

```python
>>> with db.transaction():
...     a = db.node(kind="doc")
...     a.save()
...     b = db.node(kind="doc")
...     b.save()
...     a.link(b, "related")
>>> db.count()
2
```
