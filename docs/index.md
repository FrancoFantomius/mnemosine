---
layout: home

hero:
  name: "mnemosine"
  text: "Schema-less SQLite for Python"
  tagline: "Dynamic attributes, interconnected files, and vector search with zero migrations."
  actions:
    - theme: brand
      text: Get Started
      link: /guide/getting-started
    - theme: alt
      text: API Reference
      link: /storage/index
    - theme: alt
      text: GitHub
      link: https://github.com/FrancoFantomius/mnemosine

features:
  - icon: 🧩
    title: Dynamic Schema
    details: Store arbitrary metadata in JSON columns without migrations. Automatically create generated-column indexes for fast lookups.
  - icon: 📁
    title: Content-Addressed Blobs
    details: Small text lives directly in SQLite, while binary files live in an on-disk deduplicated blob store with automatic SHA-256 hashing and GC.
  - icon: 🕸️
    title: Interconnected Graph
    details: First-class typed edges with edge metadata, recursive-CTE traversals, neighborhood discovery, and BFS shortest-path queries.
  - icon: 🔍
    title: Vector Search & Embeddings
    details: Native vector search via sqlite-vec extension with transparent brute-force fallback. Plug in any embedding model.
  - icon: ⚡
    title: Zero Migrations
    details: Add new attributes, relations, or file types on the fly. Forward-only schema versioning handles internal database upgrades effortlessly.
  - icon: 🪶
    title: Lightweight & Self-Contained
    details: Built directly on Python standard library SQLite with zero boilerplate and full type hints across all operations.
---

<div class="intro-section" style="margin-top: 3rem;">

## Welcome to mnemosine

**mnemosine** is a schema-less storage library built on top of SQLite designed for applications that outgrow simple document stores or flat relational tables. It provides a unified data layer combining:

1. **Document storage** — with JSON-backed dynamic attributes and instant indexing.
2. **File management** — with content-addressed deduplication on disk.
3. **Graph database capabilities** — with typed links and recursive graph traversals.
4. **Vector embeddings** — with fast similarity search via `sqlite-vec` (and automatic fallback).

---

## Why mnemosine?

| Challenge | Traditional Approach | mnemosine Solution |
| :--- | :--- | :--- |
| **Evolving Fields** | Alter tables / run migration scripts | Store in JSON metadata + index with `index_attribute()` |
| **Large Files** | Heavy BLOBs bloat the database | On-disk SHA-256 deduplicated blob store, metadata in DB |
| **Complex Relations** | Foreign keys & complex join tables | Typed `Link` edges with metadata and recursive graph queries |
| **AI & Vector Search** | Separate vector DB (Pinecone, Chroma, etc.) | Embedded `sqlite-vec` with zero external service dependencies |

---

## Quick Example

```python
from mnemosine import Storage

# 1. Open the storage engine
with Storage("project.db", blob_root="data/blobs") as db:
    # 2. Create a dynamic schema-less document
    doc = db.node(kind="doc", path="notes/kickoff")
    doc["title"] = "Project Plan"
    doc["tags"] = ["sqlite", "storage", "ai"]
    doc.content = "We need a resilient, hybrid storage layer."
    doc.save()

    # 3. Store a binary file (deduplicated by SHA-256 hash)
    pdf = db.file("report.pdf", mime="application/pdf")
    pdf.write(b"%PDF-1.4 sample content...")

    # 4. Link document and file with typed metadata
    doc.link(pdf, link_type="attachment", metadata={"label": "v1.0"})

    # 5. Index dynamic JSON fields on the fly
    db.index_attribute("title", as_type="TEXT")

    # 6. Graph traversal
    for neighbor in doc.neighbors(direction="outgoing"):
        print(f"Connected to: {neighbor['node'].path} via {neighbor['link'].link_type}")
```

---

## Next Steps

- **[Getting Started Guide](/guide/getting-started)** — Step-by-step walkthrough of all features.
- **[Architecture & Design](/guide/architecture)** — Deep dive into the data model and internal design.
- **[API Reference](/storage/index)** — Detailed documentation for all modules and classes.

</div>
