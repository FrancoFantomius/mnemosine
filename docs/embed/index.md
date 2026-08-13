# Module `mnemosine.embed`

## Overview

Embedding hook: the library stays model-agnostic.

The library never imports an embedding model itself. Applications inject a
callable via ``storage.embed_fn`` and the :func:`embed` function drives it,
validates the result and stores it through the vector store.

## Functions

- [embed](embed.md)
