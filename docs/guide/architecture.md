# Architecture & Design

`mnemosine` combines SQLite's ACID guarantees with modern unstructured and semi-structured storage paradigms.

---

## SQLite Data Model

The core relational schema consists of four primary tables and virtual tables:

```
┌────────────────────────────────────────────────────────┐
│                         nodes                          │
├────────────────────────────────────────────────────────┤
│ id (TEXT PRIMARY KEY)                                  │
│ kind (TEXT)                                            │
│ path (TEXT UNIQUE)                                     │
│ content (TEXT)                                         │
│ metadata (JSON)                                        │
│ embedding (BLOB)                                       │
│ created_at (TIMESTAMP)                                 │
│ updated_at (TIMESTAMP)                                 │
└────────────────────────────────────────────────────────┘
          ▲                              ▲
          │                              │
          │ source_id                    │ target_id
┌─────────┴──────────────────────────────┴───────────────┐
│                      node_links                        │
├────────────────────────────────────────────────────────┤
│ source_id (TEXT REFERENCES nodes)                      │
│ target_id (TEXT REFERENCES nodes)                      │
│ link_type (TEXT)                                       │
│ metadata (JSON)                                        │
│ created_at (TIMESTAMP)                                 │
│ PRIMARY KEY (source_id, target_id, link_type)          │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│                        blobs                           │
├────────────────────────────────────────────────────────┤
│ node_id (TEXT REFERENCES nodes)                        │
│ rel_path (TEXT)                                        │
│ sha256 (TEXT)                                          │
│ size_bytes (INTEGER)                                   │
│ mime_type (TEXT)                                       │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│                 nodes_vec (Virtual)                    │
├────────────────────────────────────────────────────────┤
│ rowid (INTEGER PRIMARY KEY)                            │
│ vector (FLOAT[N]) via sqlite-vec                       │
└────────────────────────────────────────────────────────┘
```

---

## Subsystem Architecture

| Module | Responsibility |
| :--- | :--- |
| [`mnemosine.storage`](/storage/index) | Connection lifecycle, schema setup, transactions, query dispatching |
| [`mnemosine.node`](/node/index) | Document abstraction over SQLite rows with dict-like JSON access |
| [`mnemosine.file`](/file/index) | On-disk SHA-256 blob manager with deduplication & GC |
| [`mnemosine.link`](/link/index) | Edge representations with directional semantics and metadata |
| [`mnemosine.graph`](/graph/index) | Recursive-CTE queries, neighbor exploration, BFS shortest path |
| [`mnemosine.search`](/search/index) | Unified search combining text search and vector similarity |
| [`mnemosine.vec`](/vec/index) | `sqlite-vec` virtual table interface with fallback engine |
| [`mnemosine.embed`](/embed/index) | Model-agnostic embedding hook provider |
| [`mnemosine.schema`](/schema/index) | DDL definition, table creation, generated-column indexing |
| [`mnemosine.migrations`](/migrations/index) | Versioned `user_version` migration runner |
| [`mnemosine.ids`](/ids/index) | Sortable, collision-resistant ULID identifiers |
| [`mnemosine.util`](/util/index) | JSON serializing, datetime parsing, query sanitizing |
| [`mnemosine.exceptions`](/exceptions/index) | Hierarchy of structured mnemosine exception classes |

---

## On-Disk Blob Storage Layout

Binary files are stored in a two-level content-addressed directory structure:

```
blob_root/
  └── blobs/
      ├── 4f/
      │   └── 4fa3c28b... (binary payload)
      └── 9a/
          └── 9ab103fe... (binary payload)
```

- When saving files, the content SHA-256 is computed in chunks.
- If the hash already exists on disk, no additional file write is performed (automatic deduplication).
- Deleting a node does not immediately delete the blob file to ensure safety across shared references. Calling `db.gc_blobs()` identifies unreferenced files and removes them.

---

## Vector Search & Resilient Fallback

`mnemosine` automatically attempts to load the native C extension `sqlite-vec`. If running in an environment without pre-compiled binaries for the architecture, `mnemosine` falls back to an internal numpy/pure-Python cosine distance calculation.

This ensures applications written with `mnemosine` are 100% portable across development, testing, and deployment environments.
