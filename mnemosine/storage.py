"""The Storage object: connection lifecycle, schema, factories, and queries.

A :class:`Storage` wraps a single SQLite database file, its on-disk blob
store, and the high-level object model (nodes, files, links, graph, search,
vectors). It is the main entry point of the library::

    from mnemosine import Storage
    with Storage("project.db", blob_root="data/blobs") as db:
        doc = db.node(kind="doc")
        doc["title"] = "Plan"
        doc.save()
"""

import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path

from . import vec
from .exceptions import NodeNotFound
from .file import File
from .graph import Graph
from .link import Link
from .migrations import migrate
from .node import Node
from .search import Search

_MISSING = object()


class Storage:
    def __init__(self, path="mnemosine.db", blob_root=None):
        """Create a Storage handle (no connection is opened yet).

        Call :meth:`connect` (or use the ``with`` statement) before any
        operation. File content lives in the blob store directory while node
        metadata and links live in the SQLite database.

        Args:
            path (str | os.PathLike): Path to the SQLite database file.
                Defaults to ``"mnemosine.db"``.
            blob_root (str | os.PathLike | None): Directory where file
                contents are stored. When omitted, defaults to a sibling
                directory named ``<db-stem>.blobs`` next to the database.

        Returns:
            Storage: A new, disconnected Storage.

        Example:
            >>> db = Storage("project.db", blob_root="data/blobs")
            >>> db.connect()  # doctest: +SKIP
        """
        self.path = str(path)
        if blob_root is None:
            base = Path(self.path)
            self.blob_root = base.parent / (base.stem + ".blobs")
        else:
            self.blob_root = Path(blob_root)
        self.conn = None
        self.embed_fn = None
        self.vec = vec.VectorStore(self)
        self.graph = Graph(self)
        self.search = Search(self)
        self._lock = threading.RLock()
        self._tx_depth = 0

    # ---- lifecycle --------------------------------------------------------

    def connect(self):
        """Open the database connection and prepare the schema.

        Creates the database file and blob_root directory if missing, enables
        ``foreign_keys`` and ``WAL``, sets a busy timeout, tries to load the
        sqlite-vec extension, and runs any pending migrations. Idempotent: a
        second call returns without doing anything.

        Returns:
            Storage: This storage, now connected.

        Raises:
            sqlite3.Error: If the database cannot be opened or migrated.

        Example:
            >>> db = Storage("project.db")
            >>> db.connected
            False
            >>> db.connect()
            >>> db.connected
            True
        """
        if self.conn is not None:
            return self
        parent = Path(self.path).parent
        if str(parent):
            parent.mkdir(parents=True, exist_ok=True)
        self.blob_root.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.isolation_level = None
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute("PRAGMA busy_timeout = 5000")
        self.conn.execute("PRAGMA journal_mode = WAL")
        vec.load(self.conn)
        migrate(self.conn)
        return self

    def close(self):
        """Close the database connection.

        Safe to call when already closed. After closing, call :meth:`connect`
        again to reopen.

        Returns:
            None

        Example:
            >>> db.close()
        """
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        """Support ``with Storage(...) as db:`` by connecting.

        Returns:
            Storage: The connected storage.
        """
        return self.connect()

    def __exit__(self, *exc):
        """Close the connection when leaving the ``with`` block.

        Args:
            *exc: The exception context (ignored).

        Returns:
            bool | None: Always ``None`` (exceptions propagate).
        """
        self.close()

    @property
    def connected(self) -> bool:
        """Whether the database connection is currently open.

        Returns:
            bool: ``True`` if connected.

        Example:
            >>> db.connected
            True
        """
        return self.conn is not None

    # ---- transactions -----------------------------------------------------

    @contextmanager
    def transaction(self):
        """Run a block of operations inside a single SQLite transaction.

        Starts an explicit ``BEGIN`` when it is the outermost transaction;
        nested calls join the existing transaction. Commits on success and
        rolls back on any exception (re-raising it).

        Yields:
            Storage: This storage, so the block can use ``db.transaction()``
            or just ``db``.

        Raises:
            BaseException: Any exception raised inside the block is re-raised
                after rollback.

        Example:
            >>> with db.transaction():
            ...     a = db.node(kind="doc")
            ...     a.save()
            ...     b = db.node(kind="doc")
            ...     b.save()
            ...     a.link(b, "related")
            >>> db.count()
            2
        """
        with self._lock:
            outer = self._tx_depth == 0
            if outer:
                self.conn.execute("BEGIN")
            self._tx_depth += 1
            try:
                yield self
            except BaseException:
                if outer:
                    self._tx_depth = 0
                    try:
                        self.conn.rollback()
                    except sqlite3.Error:
                        pass
                raise
            else:
                self._tx_depth -= 1
                if outer:
                    self.conn.commit()

    # ---- factories ---------------------------------------------------------

    def node(self, kind="text", path=None, metadata=None):
        """Create a new unsaved :class:`Node`.

        Does not write to the database until :meth:`Node.save` is called, so
        attributes can be set first.

        Args:
            kind (str): The node kind. Defaults to ``"text"``.
            path (str | None): Optional logical name or path.
            metadata (dict | None): Initial dynamic attributes.

        Returns:
            Node: A new unsaved node.

        Example:
            >>> doc = db.node(kind="doc", path="notes/one")
            >>> doc["title"] = "One"
            >>> doc.save()
        """
        return Node(self, kind=kind, path=path, metadata=metadata)

    def file(self, name=None, mime=None):
        """Create a new unsaved :class:`File`.

        Binary content is written to the blob store with
        :meth:`File.write`; until then the file has no content.

        Args:
            name (str | None): Logical file name or path.
            mime (str | None): MIME type (stored in metadata).

        Returns:
            File: A new unsaved file node.

        Example:
            >>> f = db.file("report.pdf", mime="application/pdf")
            >>> f.write(b"%PDF-1.4")
        """
        return File(self, name=name, mime=mime)

    def get(self, node_id, default=_MISSING):
        """Load a node (or file) by id.

        Returns a :class:`File` when the stored ``kind`` is ``"file"``,
        otherwise a :class:`Node`.

        Args:
            node_id (str): The node id.
            default (object): Value returned when the node is missing. By
                default :class:`NodeNotFound` is raised instead.

        Returns:
            Node | File | object: The loaded node/file, or ``default``.

        Raises:
            NodeNotFound: If the node does not exist and no ``default`` was
                given.

        Example:
            >>> loaded = db.get(doc.id)
            >>> loaded["title"]
            'One'
            >>> db.get("nope", default=None)
            None
        """
        row = self.conn.execute(
            "SELECT * FROM nodes WHERE id = ?", (node_id,)
        ).fetchone()
        if row is None:
            if default is not _MISSING:
                return default
            raise NodeNotFound(node_id)
        if row["kind"] == "file":
            return File.from_row(self, row)
        return Node.from_row(self, row)

    def exists(self, node_id) -> bool:
        """Check whether a node id exists.

        Args:
            node_id (str): The node id.

        Returns:
            bool: ``True`` if a node with that id exists.

        Example:
            >>> db.exists(doc.id)
            True
        """
        return (
            self.conn.execute("SELECT 1 FROM nodes WHERE id = ?", (node_id,)).fetchone()
            is not None
        )

    def list_nodes(self, kind=None, limit=1000, offset=0):
        """List nodes, newest-updated first.

        Args:
            kind (str | None): Only return nodes of this kind.
            limit (int): Maximum number of rows. Defaults to 1000.
            offset (int): Row offset for pagination.

        Returns:
            list of Node: The loaded nodes.

        Example:
            >>> nodes = db.list_nodes(kind="doc", limit=10)
        """
        sql = "SELECT id FROM nodes"
        params = []
        if kind:
            sql += " WHERE kind = ?"
            params.append(kind)
        sql += " ORDER BY updated_at DESC LIMIT ? OFFSET ?"
        params += [limit, offset]
        rows = self.conn.execute(sql, params).fetchall()
        return [self.get(r["id"]) for r in rows]

    def count(self, kind=None) -> int:
        """Count nodes, optionally of a single kind.

        Args:
            kind (str | None): Count only this kind when given.

        Returns:
            int: The number of matching nodes.

        Example:
            >>> db.count(kind="doc")
            3
        """
        sql = "SELECT COUNT(*) AS n FROM nodes"
        params = []
        if kind:
            sql += " WHERE kind = ?"
            params.append(kind)
        return self.conn.execute(sql, params).fetchone()["n"]

    # ---- internal persistence ----------------------------------------------

    def _save_node(self, node):
        """Persist a node inside a transaction.

        Internal: called by :meth:`Node.save`.

        Args:
            node (Node): The node to save.

        Returns:
            Node: The saved node.

        Example:
            >>> db._save_node(doc)
        """
        with self.transaction():
            node._save_row(self.conn)
        return node

    def _delete_node(self, node_id):
        """Delete a node and its dependent data inside a transaction.

        Internal: called by :meth:`Node.delete`. Removes the embedding, then
        the node row (links and blob row cascade via foreign keys).

        Args:
            node_id (str): The node id.

        Returns:
            None

        Example:
            >>> db._delete_node(doc.id)
        """
        with self.transaction():
            self.vec.delete(node_id)
            self.conn.execute("DELETE FROM nodes WHERE id = ?", (node_id,))

    # ---- links -------------------------------------------------------------

    def link(self, source, target, link_type="link", metadata=None):
        """Create a link between two nodes (or ids).

        Idempotent: linking the same pair with the same type returns the
        existing link. See :meth:`Link.create`.

        Args:
            source (Node | str): Source node or id.
            target (Node | str): Target node or id.
            link_type (str): The link type. Defaults to ``"link"``.
            metadata (dict | None): Optional JSON-serializable attributes.

        Returns:
            Link: The created (or existing) link.

        Example:
            >>> db.link(doc, pdf, "attachment", {"label": "v1"})
        """
        return Link.create(self, source, target, link_type, metadata)

    def unlink(self, source, target, link_type="link"):
        """Remove a link between two nodes (or ids).

        Args:
            source (Node | str): Source node or id.
            target (Node | str): Target node or id.
            link_type (str): The link type to remove.

        Returns:
            None

        Example:
            >>> db.unlink(doc, pdf, "attachment")
        """
        source_id = source.id if isinstance(source, Node) else source
        target_id = target.id if isinstance(target, Node) else target
        with self.transaction():
            self.conn.execute(
                "DELETE FROM node_links "
                "WHERE source_id = ? AND target_id = ? AND link_type = ?",
                (source_id, target_id, link_type),
            )

    def links(self, source=None, target=None, link_type=None, limit=1000):
        """Query links by endpoint and/or type.

        Any combination of filters may be given; omitted filters are
        unrestricted.

        Args:
            source (Node | str | None): Only links with this source.
            target (Node | str | None): Only links with this target.
            link_type (str | None): Only links of this type.
            limit (int): Maximum rows. Defaults to 1000.

        Returns:
            list of Link: The matching links.

        Example:
            >>> outgoing = db.links(source=doc.id)
            >>> tagged = db.links(link_type="tag", limit=50)
        """
        clauses = []
        params = []
        if source is not None:
            clauses.append("source_id = ?")
            params.append(source.id if isinstance(source, Node) else source)
        if target is not None:
            clauses.append("target_id = ?")
            params.append(target.id if isinstance(target, Node) else target)
        if link_type is not None:
            clauses.append("link_type = ?")
            params.append(link_type)
        sql = "SELECT * FROM node_links"
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " LIMIT ?"
        params.append(limit)
        rows = self.conn.execute(sql, params).fetchall()
        return [Link.from_row(self, r) for r in rows]

    def _links_for(self, node_id, direction="both", link_type=None):
        """Return links incident to a node in a given direction.

        Internal: called by :meth:`Node.links`.

        Args:
            node_id (str): The node id.
            direction (str): ``"out"``, ``"in"`` or ``"both"``.
            link_type (str | None): Optional type filter.

        Returns:
            list of Link: The matching links.

        Example:
            >>> db._links_for(doc.id, direction="out")
        """
        arms = []
        params = []
        if direction in ("out", "both"):
            cond = "source_id = ?"
            params.append(node_id)
            if link_type:
                cond += " AND link_type = ?"
                params.append(link_type)
            arms.append(f"SELECT * FROM node_links WHERE {cond}")
        if direction in ("in", "both"):
            cond = "target_id = ?"
            params.append(node_id)
            if link_type:
                cond += " AND link_type = ?"
                params.append(link_type)
            arms.append(f"SELECT * FROM node_links WHERE {cond}")
        if not arms:
            return []
        rows = self.conn.execute(" UNION ALL ".join(arms), params).fetchall()
        return [Link.from_row(self, r) for r in rows]

    # ---- dynamic schema -----------------------------------------------------

    def index_attribute(self, attr, as_type="TEXT"):
        """Add a generated column and index for a JSON metadata attribute.

        See :func:`mnemosine.schema.index_json_attribute`. Enables fast
        lookups on dynamic attributes without migrations.

        Args:
            attr (str): The metadata attribute to index.
            as_type (str): SQL type: ``TEXT``, ``INTEGER``, ``REAL`` or
                ``BLOB``. Defaults to ``TEXT``.

        Returns:
            str: The generated column name.

        Raises:
            ValueError: If ``as_type`` is not a supported SQL type.

        Example:
            >>> col = db.index_attribute("priority", as_type="INTEGER")
            >>> db.conn.execute(f"SELECT count(*) FROM nodes WHERE {col} > 3").fetchone()[0]
            0
        """
        from .schema import index_json_attribute

        return index_json_attribute(self.conn, attr, as_type)

    # ---- embeddings ----------------------------------------------------------

    def embed(self, node, text=None):
        """Compute and store an embedding for a node.

        See :func:`mnemosine.embed.embed`. Requires ``embed_fn``.

        Args:
            node (Node): The node to embed.
            text (str | None): Optional text; defaults to ``node.content``.

        Returns:
            list of float: The computed embedding.

        Raises:
            EmbeddingRequired: If ``embed_fn`` is unset or there is no text.
            VectorError: If the embedding function returns an invalid vector.

        Example:
            >>> db.embed_fn = lambda t: [1.0, 0.0]
            >>> db.embed(doc)
            [1.0, 0.0]
        """
        from . import embed as embed_module

        return embed_module.embed(self, node, text)

    # ---- blob maintenance ----------------------------------------------------

    def gc_blobs(self) -> int:
        """Delete blob files no longer referenced by any node.

        Walks the blob store, removes every file whose relative path is not
        referenced by the ``blobs`` table (and is not a temp file), then prunes
        empty directories. Return the number of files removed.

        Returns:
            int: Number of blob files deleted.

        Example:
            >>> removed = db.gc_blobs()
            >>> print(f"removed {removed} orphaned blobs")
            removed 0 orphaned blobs
        """
        if not self.blob_root.exists():
            return 0
        referenced = {
            r["rel_path"]
            for r in self.conn.execute("SELECT rel_path FROM blobs").fetchall()
        }
        removed = 0
        for path in self.blob_root.rglob("*"):
            if path.is_file():
                rel = path.relative_to(self.blob_root).as_posix()
                if rel not in referenced and not rel.startswith(".tmp"):
                    path.unlink()
                    removed += 1
        for path in sorted(
            (p for p in self.blob_root.rglob("*") if p.is_dir()), reverse=True
        ):
            try:
                path.rmdir()
            except OSError:
                pass
        return removed