# Module `mnemosine.vec`

## Overview

sqlite-vec integration with a graceful, dependency-free fallback.

If the ``sqlite-vec`` package is importable, a ``vec0`` virtual table provides
k-NN search. Otherwise vectors are stored as JSON in a plain table and searched
with a brute-force scan, so embeddings are never lost when the extension is
unavailable.

The metric and dimension are fixed on the first stored vector and recorded in
the ``vec_meta`` table; subsequent vectors must match that dimension.

## Functions

- [load](load.md)
- [_distance](_distance.md)

## Class VectorStore

- [VectorStore](VectorStore.md)
  - [VectorStore.__init__](VectorStore.__init__.md)
  - [VectorStore.conn](VectorStore.conn.md)
  - [VectorStore.available](VectorStore.available.md)
  - [VectorStore._native_table_exists](VectorStore._native_table_exists.md)
  - [VectorStore._dims](VectorStore._dims.md)
  - [VectorStore._metric](VectorStore._metric.md)
  - [VectorStore._ensure_fallback_table](VectorStore._ensure_fallback_table.md)
  - [VectorStore._ensure_native](VectorStore._ensure_native.md)
  - [VectorStore.set_vector](VectorStore.set_vector.md)
  - [VectorStore.get_vector](VectorStore.get_vector.md)
  - [VectorStore._vec_to_list](VectorStore._vec_to_list.md)
  - [VectorStore.knn](VectorStore.knn.md)
  - [VectorStore.delete](VectorStore.delete.md)
