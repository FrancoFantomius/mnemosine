# Module `mnemosine.node`

## Overview

The Node model: a schema-less document with JSON metadata.

A node is the core entity of mnemosine. It always has an ``id`` and a
``kind``, plus a JSON ``metadata`` dictionary that can hold any attributes
without any schema migration. Optional ``path`` and ``content`` fields cover
text documents; binary content is handled by the :class:`~mnemosine.file.File`
subclass.

## Class Node

- [Node](Node.md)
  - [Node.__init__](Node.__init__.md)
  - [Node.__getitem__](Node.__getitem__.md)
  - [Node.__setitem__](Node.__setitem__.md)
  - [Node.__delitem__](Node.__delitem__.md)
  - [Node.__contains__](Node.__contains__.md)
  - [Node.get](Node.get.md)
  - [Node.update](Node.update.md)
  - [Node.metadata](Node.metadata.md)
  - [Node.created_at](Node.created_at.md)
  - [Node.updated_at](Node.updated_at.md)
  - [Node.save](Node.save.md)
  - [Node.delete](Node.delete.md)
  - [Node.refresh](Node.refresh.md)
  - [Node.neighbors](Node.neighbors.md)
  - [Node.links](Node.links.md)
  - [Node.link](Node.link.md)
  - [Node.unlink](Node.unlink.md)
  - [Node.add_embedding](Node.add_embedding.md)
  - [Node.from_row](Node.from_row.md)
  - [Node._save_row](Node._save_row.md)
  - [Node.__repr__](Node.__repr__.md)
  - [Node.__eq__](Node.__eq__.md)
  - [Node.__hash__](Node.__hash__.md)
