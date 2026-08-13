"""Exceptions raised by mnemosine.

All errors raised by the library derive from :class:`MnemosineError`, so
callers can catch a single type when they want to handle every mnemosine
failure.
"""


class MnemosineError(Exception):
    """Base class for all mnemosine errors.

    Every exception defined in this module (and any future one) subclasses
    this type. Catch it to handle any library failure.

    Example:
        >>> from mnemosine import Storage, MnemosineError
        >>> try:
        ...     with Storage(":memory:"):
        ...         raise MnemosineError("boom")
        ... except MnemosineError:
        ...     print("caught")
        caught
    """


class NodeNotFound(MnemosineError):
    """Raised when a node id does not exist in the database.

    Thrown by :meth:`mnemosine.Storage.get` unless a ``default`` is supplied.

    Attributes:
        node_id (str): The id that could not be found.

    Example:
        >>> from mnemosine import Storage, NodeNotFound
        >>> with Storage(":memory:") as db:
        ...     try:
        ...         db.get("missing")
        ...     except NodeNotFound as e:
        ...         print(e.node_id)
        missing
    """

    def __init__(self, node_id):
        self.node_id = node_id
        super().__init__(f"node not found: {node_id!r}")


class NodeConflict(MnemosineError):
    """Raised when a node cannot be created because one with the id already exists.

    Reserved for future use by explicit-id insertion paths; base schema saves
    generate fresh ULIDs and therefore never conflict.

    Example:
        >>> from mnemosine import NodeConflict
        >>> raise NodeConflict("duplicate id")
        Traceback (most recent call last):
        ...
        mnemosine.exceptions.NodeConflict: duplicate id
    """


class LinkExists(MnemosineError):
    """Raised when a duplicate link would be created.

    The base schema treats ``(source_id, target_id, link_type)`` as a primary
    key. :meth:`mnemosine.Link.create` is idempotent and returns the existing
    link instead of raising; this exception remains for callers that pass
    ``INSERT``-style semantics.

    Example:
        >>> from mnemosine import LinkExists
        >>> raise LinkExists("link already present")
        Traceback (most recent call last):
        ...
        mnemosine.exceptions.LinkExists: link already present
    """


class FileNotFound(MnemosineError):
    """Raised when a File has no stored content to read.

    Either the file node has never had content written (``write()`` not yet
    called) or the underlying blob file is missing from the blob store.

    Attributes:
        node_id (str): The id of the file node without content.

    Example:
        >>> from mnemosine import Storage, FileNotFound
        >>> with Storage(":memory:") as db:
        ...     f = db.file("empty.txt")
        ...     f.save()
        ...     try:
        ...         f.read()
        ...     except FileNotFound:
        ...         print("no content yet")
        no content yet
    """

    def __init__(self, node_id):
        self.node_id = node_id
        super().__init__(f"file has no stored content: {node_id!r}")


class BlobStoreError(MnemosineError):
    """Raised when the on-disk blob store fails (I/O, permissions, corruption).

    Reserved for blob-store-level failures such as an unwritable ``blob_root``
    or an unreadable blob file.

    Example:
        >>> from mnemosine import BlobStoreError
        >>> raise BlobStoreError("blob store is unwritable")
        Traceback (most recent call last):
        ...
        mnemosine.exceptions.BlobStoreError: blob store is unwritable
    """


class VectorError(MnemosineError):
    """Raised for vector-related problems.

    Covers dimension mismatches, unsupported metrics, malformed vectors and
    any other error produced by the vector store (native ``sqlite-vec`` or the
    brute-force fallback).

    Example:
        >>> from mnemosine import VectorError
        >>> raise VectorError("dimension mismatch: stored vectors are 3d, got 2d")
        Traceback (most recent call last):
        ...
        mnemosine.exceptions.VectorError: dimension mismatch: stored vectors are 3d, got 2d
    """


class EmbeddingRequired(VectorError):
    """Raised when an embedding is requested but cannot be produced.

    Two situations: no ``embed_fn`` has been configured on the ``Storage``, or
    the node has no text content to embed.

    Example:
        >>> from mnemosine import Storage, EmbeddingRequired
        >>> with Storage(":memory:") as db:
        ...     doc = db.node(kind="doc")
        ...     doc.save()
        ...     try:
        ...         doc.add_embedding()
        ...     except EmbeddingRequired:
        ...         print("set storage.embed_fn first")
        set storage.embed_fn first
    """
