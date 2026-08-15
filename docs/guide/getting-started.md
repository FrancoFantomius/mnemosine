# Getting Started with mnemosine

This guide will walk you through installing **mnemosine**, creating your first storage instance, managing documents and dynamic attributes, storing files with content-addressing, linking nodes into a graph, and running vector similarity searches.

---

## 1. Installation

`mnemosine` requires Python 3.10+ and SQLite 3.38+ (with SQLite 3.41+ recommended for `sqlite-vec`).

### From PyPI / Local Clone
```bash
pip install mnemosine
```

Or install in editable mode for local development:
```bash
git clone https://github.com/FrancoFantomius/mnemosine.git
cd mnemosine
pip install -e .
```

To install development dependencies (including `pytest`):
```bash
pip install -e .[dev]
```

---

## 2. Storage Lifecycle

The central entry point in `mnemosine` is the [`Storage`](/storage/Storage) class. It manages SQLite connection pooling, transactions, blob filesystem roots, and sub-systems.

```python
from mnemosine import Storage

# Using context manager (recommended: auto-commits and closes)
with Storage("workspace.db", blob_root="data/blobs") as db:
    print(f"Connected: {db.connected}")
    # perform operations...
```

You can also use in-memory databases for tests:
```python
with Storage(":memory:") as db:
    # fast in-memory operations
    pass
```

---

## 3. Dynamic Nodes & JSON Schema

In `mnemosine`, documents and entities are represented as [`Node`](/node/Node) instances. Each node has:
- `id`: A unique ULID-style sortable identifier.
- `kind`: A string categorization tag (e.g. `'doc'`, `'user'`, `'task'`).
- `path`: An optional unique logical path (e.g. `'notes/release-v1'`).
- `content`: Optional text body.
- `metadata`: Arbitrary JSON dictionary for dynamic properties.

### Creating and Modifying Nodes

```python
# Create an unsaved node
note = db.node(kind="note", path="daily/2026-08-15")

# Dynamic attributes (stored inside JSON metadata)
note["title"] = "Daily Standup"
note["priority"] = 1
note["tags"] = ["engineering", "sqlite"]

# Text content
note.content = "Discussed migration-free database architectures."

# Persist to SQLite
note.save()
```

### Retrieving Nodes

```python
# Lookup by ID
node = db.get("01J5K4M9...")

# Lookup by logical path
node = db.get(path="daily/2026-08-15")

# List all nodes of a kind
notes = db.list_nodes(kind="note")
```

---

## 4. Indexing Dynamic Attributes

Because `metadata` is stored as JSON in SQLite, you can query or filter by any property. For high-performance queries on specific attributes, use generated columns:

```python
# Create a generated column and index on metadata->>'priority'
db.index_attribute("priority", as_type="INTEGER")

# Create a generated column and index on metadata->>'title'
db.index_attribute("title", as_type="TEXT")
```

This creates an indexed generated column transparently without altering your data model or requiring external database migrations.

---

## 5. File & Blob Storage

Large binary files (PDFs, images, datasets) should not bloat the SQLite database file. `mnemosine` provides a content-addressed on-disk blob store through [`File`](/file/File).

```python
# Create a FileNode
file_node = db.file("uploads/report.pdf", mime="application/pdf")

# Write binary content (automatically hashes SHA-256 and writes to disk)
file_node.write(b"%PDF-1.4 binary data...")

print(file_node.sha256)
print(file_node.size_bytes)
```

### Content Deduplication and Garbage Collection

If two files contain identical content, only a single copy is stored on disk under `blob_root/blobs/<sha256[:2]>/<sha256>`.

When nodes or files are deleted, clean up unreferenced blobs with:
```python
removed_count = db.gc_blobs()
print(f"Cleaned up {removed_count} orphaned blobs")
```

---

## 6. Graph Relationships & Queries

Nodes and files can be linked with typed, directional edges that also carry arbitrary metadata.

### Creating Links

```python
task = db.node(kind="task", path="tasks/build-docs")
task["status"] = "in-progress"
task.save()

# Link note -> task
note.link(task, link_type="references", metadata={"confidence": 0.95})
```

### Traversing the Graph

```python
# Find immediate neighbors
for neighbor in note.neighbors(direction="outgoing", link_type="references"):
    target_node = neighbor["node"]
    link = neighbor["link"]
    print(f"{note.path} -> {link.link_type} -> {target_node.path}")

# Shortest path between two nodes (BFS)
path = db.graph.path(note, task)

# Subgraph extraction up to N hops
subgraph = db.graph.subgraph(note, max_depth=3)
```

---

## 7. Vector Search & Embeddings

`mnemosine` includes vector search capabilities backed by [`sqlite-vec`](https://github.com/asg017/sqlite-vec). If the extension cannot be loaded on a system, `mnemosine` seamlessly falls back to a brute-force cosine similarity engine so your application never crashes.

### Registering an Embedding Function

```python
# Bring your own embedding model (e.g. fastembed, sentence-transformers, OpenAI)
def embed_text(text: str) -> list[float]:
    return [0.12, -0.45, 0.78, ...] # Return vector floats

db.embed_fn = embed_text
```

### Generating Embeddings for Nodes

```python
# Embeds the node's content (or custom text) and stores the vector
note.add_embedding()
```

### Running k-Nearest Neighbor (k-NN) Vector Search

```python
query_vector = embed_text("database architecture notes")

results = db.search.vector(query_vector, top_k=5)
for match in results:
    matched_node = match["node"]
    distance = match["distance"]
    print(f"[{distance:.4f}] {matched_node.path}: {matched_node['title']}")
```

---

## 8. Summary & Next Steps

You now have a full overview of what `mnemosine` can do! Check out:
- [Architecture & Design](/guide/architecture) for details on the SQLite schema and storage internals.
- [Storage API Reference](/storage/index) for complete class documentation.
