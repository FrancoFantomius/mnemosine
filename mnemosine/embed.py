"""Embedding hook: the library stays model-agnostic.

The library never imports an embedding model itself. Applications inject a
callable via ``storage.embed_fn`` and the :func:`embed` function drives it,
validates the result and stores it through the vector store.
"""

from .exceptions import EmbeddingRequired, VectorError


def embed(storage, node, text=None):
    """Compute and store an embedding for ``node``.

    Uses ``storage.embed_fn`` to turn text into a vector, validates that the
    result is a non-empty sequence of numbers, and stores it via
    :meth:`mnemosine.vec.VectorStore.set_vector`. When ``text`` is omitted the
    node's ``content`` is embedded.

    Args:
        storage (Storage): The storage whose ``embed_fn`` is used.
        node (Node): The node to embed.
        text (str | None): Explicit text to embed. Defaults to
            ``node.content``.

    Returns:
        list of float: The computed embedding vector.

    Raises:
        EmbeddingRequired: If ``storage.embed_fn`` is not set, or there is no
            text to embed.
        VectorError: If ``embed_fn`` returns something other than a
            non-empty sequence of numbers.

    Example:
        >>> db.embed_fn = lambda text: [1.0 if "storage" in text else 0.0, 0.0]
        >>> from mnemosine.embed import embed
        >>> embed(db, doc)
        [1.0, 0.0]
    """
    if storage.embed_fn is None:
        raise EmbeddingRequired(
            "no embedding function configured; set storage.embed_fn = lambda text: vector"
        )
    text = text if text is not None else node.content
    if not text:
        raise EmbeddingRequired("node has no content and no text was provided")
    vector = storage.embed_fn(text)
    if not isinstance(vector, (list, tuple)) or not vector:
        raise VectorError("embed_fn must return a non-empty sequence of floats")
    storage.vec.set_vector(node.id, vector)
    return vector