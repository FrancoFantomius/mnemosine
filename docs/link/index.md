# Module `mnemosine.link`

## Overview

The Link model: a typed, metadata-carrying edge between two nodes.

A link connects a source node to a target node with a ``link_type`` and an
optional JSON ``metadata`` payload (weights, labels, timestamps, ...). The
underlying ``node_links`` table treats ``(source_id, target_id, link_type)``
as a primary key, so linking the same pair twice with the same type is
idempotent.

## Functions

- [_as_id](_as_id.md)

## Class Link

- [Link](Link.md)
  - [Link.__init__](Link.__init__.md)
  - [Link.metadata](Link.metadata.md)
  - [Link.__getitem__](Link.__getitem__.md)
  - [Link.create](Link.create.md)
  - [Link.from_row](Link.from_row.md)
  - [Link.delete](Link.delete.md)
  - [Link.source](Link.source.md)
  - [Link.target](Link.target.md)
  - [Link.__repr__](Link.__repr__.md)
