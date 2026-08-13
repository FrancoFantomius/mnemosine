# Module `mnemosine.storage`

## Overview

The Storage object: connection lifecycle, schema, factories, and queries.

A :class:`Storage` wraps a single SQLite database file, its on-disk blob
store, and the high-level object model (nodes, files, links, graph, search,
vectors). It is the main entry point of the library::

from mnemosine import Storage
with Storage("project.db", blob_root="data/blobs") as db:
doc = db.node(kind="doc")
doc["title"] = "Plan"
doc.save()

## Class Storage

- [Storage](Storage.md)
  - [Storage.__init__](Storage.__init__.md)
  - [Storage.connect](Storage.connect.md)
  - [Storage.close](Storage.close.md)
  - [Storage.__enter__](Storage.__enter__.md)
  - [Storage.__exit__](Storage.__exit__.md)
  - [Storage.connected](Storage.connected.md)
  - [Storage.transaction](Storage.transaction.md)
  - [Storage.node](Storage.node.md)
  - [Storage.file](Storage.file.md)
  - [Storage.get](Storage.get.md)
  - [Storage.exists](Storage.exists.md)
  - [Storage.list_nodes](Storage.list_nodes.md)
  - [Storage.count](Storage.count.md)
  - [Storage._save_node](Storage._save_node.md)
  - [Storage._delete_node](Storage._delete_node.md)
  - [Storage.link](Storage.link.md)
  - [Storage.unlink](Storage.unlink.md)
  - [Storage.links](Storage.links.md)
  - [Storage._links_for](Storage._links_for.md)
  - [Storage.index_attribute](Storage.index_attribute.md)
  - [Storage.embed](Storage.embed.md)
  - [Storage.gc_blobs](Storage.gc_blobs.md)
