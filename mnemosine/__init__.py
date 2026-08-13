"""mnemosine: schema-less SQLite storage for larger projects.

Dynamic JSON attributes on nodes, typed links between them, an on-disk blob
store for files, and vector search via sqlite-vec.
"""

from .exceptions import (
    BlobStoreError,
    EmbeddingRequired,
    FileNotFound,
    LinkExists,
    MnemosineError,
    NodeConflict,
    NodeNotFound,
    VectorError,
)
from .file import File
from .link import Link
from .node import Node
from .storage import Storage

__version__ = "0.1.0"

__all__ = [
    "BlobStoreError",
    "EmbeddingRequired",
    "File",
    "FileNotFound",
    "Link",
    "LinkExists",
    "MnemosineError",
    "Node",
    "NodeConflict",
    "NodeNotFound",
    "Storage",
    "VectorError",
    "__version__",
]