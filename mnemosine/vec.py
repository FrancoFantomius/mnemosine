"""sqlite-vec integration with a graceful, dependency-free fallback.

If the ``sqlite-vec`` package is importable, a ``vec0`` virtual table provides
k-NN search. Otherwise vectors are stored as JSON in a plain table and searched
with a brute-force scan, so embeddings are never lost when the extension is
unavailable.

The metric and dimension are fixed on the first stored vector and recorded in
the ``vec_meta`` table; subsequent vectors must match that dimension.
"""

import json
import math

from .exceptions import VectorError
from .util import loads

VEC_AVAILABLE = False
_imported = False
_import_error = None
_vec_module = None

METRICS = {"cosine", "l2", "dot"}


def load(conn) -> bool:
    """Load the sqlite-vec extension into ``conn``.

    The ``sqlite_vec`` package import is attempted only once, but the
    extension itself must be registered on every connection, so this should be
    called for each new connection (``Storage.connect`` does this
    automatically).

    Args:
        conn (sqlite3.Connection): The connection to load the extension into.

    Returns:
        bool: ``True`` if the extension is now usable on ``conn``, ``False``
        if it could not be imported or loaded (the library falls back to the
        brute-force store in that case).

    Example:
        >>> import sqlite3
        >>> from mnemosine import vec
        >>> conn = sqlite3.connect(":memory:")
        >>> vec.load(conn)
        True
    """
    global VEC_AVAILABLE, _imported, _import_error, _vec_module
    if not _imported:
        _imported = True
        try:
            import sqlite_vec

            _vec_module = sqlite_vec
        except Exception as exc:
            _import_error = exc
    if _import_error is not None:
        return False
    try:
        conn.enable_load_extension(True)
        _vec_module.load(conn)
        VEC_AVAILABLE = True
        return True
    except Exception:
        return False


class VectorStore:
    def __init__(self, storage):
        """Wrap a Storage and expose vector operations.

        Access a ``VectorStore`` through ``storage.vec`` rather than
        constructing it directly.

        Args:
            storage (Storage): The owning storage.

        Returns:
            VectorStore: A vector store view over the storage.
        """
        self._storage = storage

    @property
    def conn(self):
        """The underlying database connection.

        Returns:
            sqlite3.Connection: The connection owned by the storage.

        Example:
            >>> db.vec.conn  # doctest: +SKIP
            <sqlite3.Connection object at 0x...>
        """
        return self._storage.conn

    @property
    def available(self) -> bool:
        """Whether the native sqlite-vec extension is loaded.

        Returns:
            bool: ``True`` when k-NN runs on the ``vec0`` virtual table,
            ``False`` when the brute-force fallback is used.

        Example:
            >>> db.vec.available
            True
        """
        return VEC_AVAILABLE

    def _native_table_exists(self) -> bool:
        """Return whether the ``nodes_vec`` virtual table has been created.

        Internal guard used before touching the native table, which only
        exists once a vector has been stored.

        Returns:
            bool: ``True`` if the table exists.

        Example:
            >>> db.vec._native_table_exists()
            False
        """
        return (
            self.conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'nodes_vec'"
            ).fetchone()
            is not None
        )

    # ---- internals -----------------------------------------------------

    def _dims(self):
        """Return the recorded embedding dimension, or ``None``.

        Returns:
            int | None: The dimension recorded in ``vec_meta``.

        Example:
            >>> db.vec._dims()
            3
        """
        row = self.conn.execute("SELECT v FROM vec_meta WHERE k = 'dims'").fetchone()
        return int(row["v"]) if row else None

    def _metric(self):
        """Return the recorded distance metric (defaults to ``"cosine"``).

        Returns:
            str: The metric stored in ``vec_meta``, or ``"cosine"``.

        Example:
            >>> db.vec._metric()
            'cosine'
        """
        row = self.conn.execute("SELECT v FROM vec_meta WHERE k = 'metric'").fetchone()
        return row["v"] if row else "cosine"

    def _ensure_fallback_table(self):
        """Create the fallback table if it does not exist.

        Creates ``embedding_fallback(node_id, dims, vec)``, used when the
        sqlite-vec extension is unavailable.

        Returns:
            None

        Example:
            >>> db.vec._ensure_fallback_table()  # doctest: +SKIP
        """
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS embedding_fallback ("
            " node_id TEXT PRIMARY KEY, dims INTEGER NOT NULL, vec TEXT NOT NULL)"
        )

    def _ensure_native(self, dims: int, metric: str):
        """Create the ``nodes_vec`` virtual table and record metadata.

        Fixes the table dimension/metric on first use; a later vector with a
        different dimension raises. Validates the metric against
        :data:`METRICS`.

        Args:
            dims (int): Embedding dimension.
            metric (str): Distance metric for the ``vec0`` table.

        Returns:
            None

        Raises:
            VectorError: If ``metric`` is unsupported or the dimension
                conflicts with previously stored vectors.

        Example:
            >>> db.vec._ensure_native(3, "cosine")  # doctest: +SKIP
        """
        if metric not in METRICS:
            raise VectorError(
                f"unsupported metric {metric!r}, choose from {sorted(METRICS)}"
            )
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS vec_meta(k TEXT PRIMARY KEY, v TEXT)"
        )
        stored = self._dims()
        if stored is not None and stored != dims:
            raise VectorError(
                f"vector dimension mismatch: stored vectors are {stored}d, "
                f"got {dims}d. Use a fixed embedding size."
            )
        self.conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS nodes_vec USING vec0("
            f"node_id TEXT PRIMARY KEY, vec FLOAT[{dims}] distance_metric={metric})"
        )
        if stored is None:
            self.conn.execute(
                "INSERT INTO vec_meta(k, v) VALUES ('dims', ?)", (str(dims),)
            )
            self.conn.execute(
                "INSERT INTO vec_meta(k, v) VALUES ('metric', ?)", (metric,)
            )

    # ---- public API -----------------------------------------------------

    def set_vector(self, node_id: str, vector, metric: str = "cosine") -> None:
        """Store (or replace) the embedding for a node.

        On the native path the vector is upserted into ``nodes_vec`` (delete +
        insert); on the fallback path it is upserted into
        ``embedding_fallback``. Also flips the node's ``embedding`` flag to 1.

        Args:
            node_id (str): The node id.
            vector (sequence of float): The embedding vector. Must be
                non-empty and match the recorded dimension.
            metric (str): Distance metric (native path only). Defaults to
                ``"cosine"``.

        Returns:
            None

        Raises:
            VectorError: If ``vector`` is empty/not a sequence, the metric is
                unsupported, or the dimension conflicts.

        Example:
            >>> db.vec.set_vector(doc.id, [1.0, 0.0, 0.0])
        """
        if not isinstance(vector, (list, tuple)) or not vector:
            raise VectorError("vector must be a non-empty sequence of floats")
        floats = [float(x) for x in vector]
        if VEC_AVAILABLE:
            self._ensure_native(len(floats), metric)
            self.conn.execute("DELETE FROM nodes_vec WHERE node_id = ?", (node_id,))
            self.conn.execute(
                "INSERT INTO nodes_vec(node_id, vec) VALUES (?, ?)",
                (node_id, json.dumps(floats)),
            )
        else:
            self._ensure_fallback_table()
            self.conn.execute(
                "INSERT INTO embedding_fallback(node_id, dims, vec) VALUES (?, ?, ?) "
                "ON CONFLICT(node_id) DO UPDATE SET dims = excluded.dims, "
                "vec = excluded.vec",
                (node_id, len(floats), json.dumps(floats)),
            )
        self.conn.execute("UPDATE nodes SET embedding = 1 WHERE id = ?", (node_id,))

    def get_vector(self, node_id: str):
        """Return the stored embedding for a node, or ``None``.

        Args:
            node_id (str): The node id.

        Returns:
            list of float | None: The embedding as a Python list, or ``None``
            if the node has no stored vector.

        Example:
            >>> db.vec.get_vector(doc.id)
            [1.0, 0.0, 0.0]
        """
        if VEC_AVAILABLE:
            if not self._native_table_exists():
                return None
            row = self.conn.execute(
                "SELECT vec FROM nodes_vec WHERE node_id = ?", (node_id,)
            ).fetchone()
            return self._vec_to_list(row["vec"]) if row else None
        self._ensure_fallback_table()
        row = self.conn.execute(
            "SELECT vec FROM embedding_fallback WHERE node_id = ?", (node_id,)
        ).fetchone()
        return loads(row["vec"]) if row else None

    @staticmethod
    def _vec_to_list(raw):
        """Convert a stored vector (bytes or JSON) into a Python list.

        ``sqlite-vec`` returns raw little-endian float32 bytes; the fallback
        table stores JSON text. Both are handled here.

        Args:
            raw (bytes | str): The raw stored vector.

        Returns:
            list of float: The decoded vector.

        Example:
            >>> VectorStore._vec_to_list(b'\\x00\\x00\\x80?')
            [1.0]
        """
        if isinstance(raw, bytes):
            import struct

            n = len(raw) // 4
            return list(struct.unpack("<%df" % n, raw))
        return loads(raw)

    def knn(self, vector, top_k: int = 10, metric: str = "cosine"):
        """Return the ``top_k`` nearest embeddings to ``vector``.

        Native path: ``vec0`` k-NN query returning ``(node_id, distance)``.
        Fallback path: brute-force scan with :func:`_distance`. Result items
        are ordered nearest-first.

        Args:
            vector (sequence of float): The query embedding.
            top_k (int): Number of results. Defaults to 10.
            metric (str): ``"cosine"`` (default), ``"l2"`` or ``"dot"``.

        Returns:
            list of dict: Each item has ``node_id`` (str) and ``distance``
            (float). Empty when no embeddings are stored.

        Raises:
            VectorError: If ``top_k < 1`` or the vector dimension conflicts.

        Example:
            >>> db.vec.knn([1.0, 0.0, 0.0], top_k=2)
            [{'node_id': '01G...', 'distance': 0.0}, ...]
        """
        if top_k < 1:
            raise VectorError("top_k must be >= 1")
        floats = [float(x) for x in vector]
        if VEC_AVAILABLE:
            if not self._native_table_exists():
                return []
            dims = self._dims()
            if dims is not None and len(floats) != dims:
                raise VectorError(
                    f"vector dimension mismatch: stored vectors are {dims}d, "
                    f"got {len(floats)}d"
                )
            rows = self.conn.execute(
                "SELECT node_id, distance FROM nodes_vec WHERE vec MATCH ? AND k = ?",
                (json.dumps(floats), top_k),
            ).fetchall()
            return [{"node_id": r["node_id"], "distance": r["distance"]} for r in rows]

        self._ensure_fallback_table()
        rows = self.conn.execute(
            "SELECT node_id, vec FROM embedding_fallback"
        ).fetchall()
        scored = [
            (_distance(floats, loads(r["vec"]), metric), r["node_id"]) for r in rows
        ]
        scored.sort(key=lambda t: t[0])
        return [
            {"node_id": node_id, "distance": distance}
            for distance, node_id in scored[:top_k]
        ]

    def delete(self, node_id: str) -> None:
        """Remove the embedding for a node and clear its ``embedding`` flag.

        Touches both the native and fallback tables so the vector is removed
        whichever path stored it. Does not delete the node itself.

        Args:
            node_id (str): The node id.

        Returns:
            None

        Example:
            >>> db.vec.delete(doc.id)
        """
        if VEC_AVAILABLE and self._native_table_exists():
            self.conn.execute("DELETE FROM nodes_vec WHERE node_id = ?", (node_id,))
        self._ensure_fallback_table()
        self.conn.execute(
            "DELETE FROM embedding_fallback WHERE node_id = ?", (node_id,)
        )
        self.conn.execute("UPDATE nodes SET embedding = 0 WHERE id = ?", (node_id,))


def _distance(a, b, metric: str) -> float:
    """Compute a distance between two same-length vectors.

    Supports ``l2`` (Euclidean), ``dot`` (negated dot product) and
    ``cosine`` (1 - cosine similarity; returns 1.0 if either vector has zero
    magnitude).

    Args:
        a (sequence of float): First vector.
        b (sequence of float): Second vector.
        metric (str): ``"l2"``, ``"dot"`` or ``"cosine"``.

    Returns:
        float: The distance. Lower means closer.

    Raises:
        VectorError: If the vectors have different lengths.

    Example:
        >>> from mnemosine.vec import _distance
        >>> round(_distance([1, 0], [1, 0], "cosine"), 3)
        0.0
    """
    if len(a) != len(b):
        raise VectorError("vector dimension mismatch during scan")
    if metric == "l2":
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
    dot = sum(x * y for x, y in zip(a, b))
    if metric == "dot":
        return -dot
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 1.0
    return 1.0 - dot / (na * nb)