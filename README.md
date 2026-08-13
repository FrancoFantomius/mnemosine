# mnemosine

A schema-less SQLite storage library for larger projects: dynamic
attributes, interconnected files, and vector search.

- **Dynamic schema** — arbitrary attributes live in a JSON metadata column;
  no migrations for new fields, and generated-column indexes for fast lookups.
- **Text and files** — small text is stored in the database; binary content is
  stored on disk in a deduplicated, content-addressed blob store.
- **Interconnected nodes** — typed, metadata-carrying links plus recursive-CTE
  graph traversal (neighbors, subgraph, shortest path).
- **Embeddings** — vector search via [sqlite-vec] (a core dependency) with a
  built-in brute-force fallback, so data is never lost if the extension fails to load.

[sqlite-vec]: https://github.com/asg017/sqlite-vec

## Requirements

- Python 3.10+
- SQLite 3.38+ for built-in JSON (3.41+ recommended for `sqlite-vec`)

## Installation

From this repository:

```bash
pip install -e .
```

From GitHub:

```bash
pip install git+https://github.com/FrancoFantomius/mnemosine.git
```

Extras needed to run the test suite (pytest):

```bash
pip install -e .[dev]
```

## Quickstart

```python
from mnemosine import Storage

with Storage("project.db", blob_root="data/blobs") as db:
    # 1. Schema-less documents
    doc = db.node(kind="doc")
    doc["title"] = "Project plan"
    doc["tags"] = ["sqlite", "storage"]
    doc.content = "We need a storage layer."
    doc.save()

    # 2. Files (deduplicated by content hash, stored on disk)
    pdf = db.file("report.pdf", mime="application/pdf")
    pdf.write(b"%PDF-1.4 fake content")
    print(pdf.sha256, pdf.size_bytes)

    # 3. Interconnections
    doc.link(pdf, link_type="attachment", metadata={"label": "v1"})
    doc.link(other, link_type="relation", metadata={"label": "cites"})
    print([n["node"].path for n in doc.neighbors()])

    # 4. Vector search (inject any embedder, e.g. sentence-transformers)
    db.embed_fn = lambda text: my_model.encode(text)  # noqa
    doc.add_embedding()
    for hit in db.search.vector(my_model.encode("storage design")):
        print(hit["node"].id, round(hit["distance"], 4))

    # 5. Graph queries
    path = db.graph.path(doc, other)
    subgraph = db.graph.subgraph(doc, max_depth=3)
```

## Data model

```
nodes(id, kind, path, content, metadata, embedding, created_at, updated_at)
node_links(source_id, target_id, link_type, metadata, created_at)
blobs(node_id, rel_path, sha256, size_bytes, mime_type)
nodes_vec  (sqlite-vec virtual table, created on first embed)
```

- `nodes.metadata` is a JSON object — the dynamic schema. Add attributes freely,
  then index them with `db.index_attribute("title", as_type="TEXT")` which
  creates a generated column + index.
- `node_links` is a typed junction table (`PRIMARY KEY (source_id, target_id,
  link_type)`) supporting N:1, M:N, self-references, and metadata on edges.
- `blobs` tracks content stored on disk under
  `blob_root/blobs/<sha256[:2]>/<sha256>`. Identical content shares one file;
  `db.gc_blobs()` removes orphaned files after deletions.

## Documentation

https://github.com/FrancoFantomius/mnemosine/tree/main/docs

## Running tests

```bash
python -m pytest
```

`sqlite-vec` is a core dependency, but the fallback path is still covered by
the test suite (tests exercise both the native extension and the fallback).

## Architecture

| Module        | Responsibility                                        |
| ------------- | ----------------------------------------------------- |
| `storage`     | Connection lifecycle, transactions, factories, queries |
| `node`        | Schema-less document model (JSON metadata)            |
| `file`        | Blob store: streaming write, hashing, dedup, GC       |
| `link`        | Typed edges with metadata                             |
| `graph`       | Recursive-CTE traversal, BFS shortest path            |
| `search`      | LIKE text search + vector k-NN                        |
| `vec`         | sqlite-vec loader, vec table, fallback store          |
| `embed`       | Model-agnostic embedding hook (`storage.embed_fn`)    |
| `schema`      | Base DDL + generated-column JSON indexing             |
| `migrations`  | Versioned, forward-only migrations (`user_version`)   |
| `ids`         | ULID-style identifiers                                |
| `util`        | JSON/timestamp/LIKE-escaping helpers                  |
