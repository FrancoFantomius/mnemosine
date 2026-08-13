# Module `mnemosine.search`

## Overview

Search: LIKE-based text search and vector k-NN.

Exposes :class:`Search` (via ``storage.search``) with a text search over the
``content``/``path``/``metadata`` columns and a vector k-NN search that
delegates to :class:`mnemosine.vec.VectorStore`.

## Class Search

- [Search](Search.md)
  - [Search.__init__](Search.__init__.md)
  - [Search.text](Search.text.md)
  - [Search.vector](Search.vector.md)
