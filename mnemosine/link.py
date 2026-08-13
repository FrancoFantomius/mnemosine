"""The Link model: a typed, metadata-carrying edge between two nodes.

A link connects a source node to a target node with a ``link_type`` and an
optional JSON ``metadata`` payload (weights, labels, timestamps, ...). The
underlying ``node_links`` table treats ``(source_id, target_id, link_type)``
as a primary key, so linking the same pair twice with the same type is
idempotent.
"""

from .node import Node
from .util import dumps, loads, utcnow


def _as_id(obj):
    """Resolve a Node instance or id string to an id.

    Args:
        obj (Node | str): A node or its id.

    Returns:
        str: The node id.

    Example:
        >>> from mnemosine.link import _as_id
        >>> _as_id("abc")
        'abc'
    """
    return obj.id if isinstance(obj, Node) else str(obj)


class Link:
    def __init__(self, storage, source_id, target_id, link_type, metadata=None, created_at=None):
        """Create an in-memory Link.

        Normal code should use :meth:`Link.create`,
        :meth:`mnemosine.Storage.link` or :meth:`mnemosine.Node.link` instead.

        Args:
            storage (Storage): The owning storage.
            source_id (str): The source node id.
            target_id (str): The target node id.
            link_type (str): The link type.
            metadata (dict | None): Optional link attributes.
            created_at (str | None): ISO-8601 timestamp; defaults to now when
                created via :meth:`Link.create`.

        Returns:
            Link: The new link object.
        """
        self._storage = storage
        self.source_id = source_id
        self.target_id = target_id
        self.link_type = link_type
        self._metadata = dict(metadata or {})
        self._created_at = created_at

    @property
    def metadata(self):
        """The link's attribute dictionary.

        Returns:
            dict: The link metadata (live reference).

        Example:
            >>> link.metadata["weight"] = 0.8
        """
        return self._metadata

    def __getitem__(self, key):
        """Read a link attribute.

        Args:
            key (str): The attribute name.

        Returns:
            object: The stored value.

        Raises:
            KeyError: If ``key`` is absent.

        Example:
            >>> link["label"]
            'cites'
        """
        return self._metadata[key]

    @classmethod
    def create(cls, storage, source, target, link_type="link", metadata=None):
        """Create and persist a link.

        Idempotent: if a link with the same source, target and type already
        exists, the existing link is returned instead of raising a duplicate
        key error. Wrapped in a transaction.

        Args:
            storage (Storage): The owning storage.
            source (Node | str): Source node or id.
            target (Node | str): Target node or id.
            link_type (str): The link type. Defaults to ``"link"``.
            metadata (dict | None): Optional JSON-serializable attributes.

        Returns:
            Link: The created (or pre-existing) link.

        Raises:
            sqlite3.IntegrityError: If either endpoint does not exist and
                foreign keys are enforced.

        Example:
            >>> link = Link.create(db, a, b, "relation", {"label": "cites"})
            >>> print(link.source_id, "->", link.target_id)
            ... # doctest: +SKIP
        """
        source_id = _as_id(source)
        target_id = _as_id(target)
        with storage.transaction():
            cur = storage.conn.execute(
                "INSERT OR IGNORE INTO node_links "
                "(source_id, target_id, link_type, metadata, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (source_id, target_id, link_type, dumps(metadata), utcnow()),
            )
            if cur.rowcount == 0:
                row = storage.conn.execute(
                    "SELECT * FROM node_links "
                    "WHERE source_id = ? AND target_id = ? AND link_type = ?",
                    (source_id, target_id, link_type),
                ).fetchone()
                return cls.from_row(storage, row)
        return cls(storage, source_id, target_id, link_type, metadata)

    @classmethod
    def from_row(cls, storage, row):
        """Build a Link from a ``node_links`` row.

        Internal helper.

        Args:
            storage (Storage): The owning storage.
            row (sqlite3.Row): A row from the ``node_links`` table.

        Returns:
            Link: The loaded link.

        Example:
            >>> row = db.conn.execute("SELECT * FROM node_links").fetchone()
            >>> Link.from_row(db, row)
            <Link ...>
        """
        return cls(
            storage,
            row["source_id"],
            row["target_id"],
            row["link_type"],
            loads(row["metadata"]),
            row["created_at"],
        )

    def delete(self):
        """Remove this link from the database.

        Returns:
            None

        Example:
            >>> link.delete()
        """
        with self._storage.transaction():
            self._storage.conn.execute(
                "DELETE FROM node_links "
                "WHERE source_id = ? AND target_id = ? AND link_type = ?",
                (self.source_id, self.target_id, self.link_type),
            )

    def source(self):
        """Load and return the source node.

        Returns:
            Node: The source node object.

        Raises:
            NodeNotFound: If the source node was deleted.

        Example:
            >>> link.source()
            <Node id='...' kind='doc'>
        """
        return self._storage.get(self.source_id)

    def target(self):
        """Load and return the target node.

        Returns:
            Node: The target node object.

        Raises:
            NodeNotFound: If the target node was deleted.

        Example:
            >>> link.target()
            <Node id='...' kind='doc'>
        """
        return self._storage.get(self.target_id)

    def __repr__(self):
        """A short, readable representation of the link.

        Returns:
            str: ``<Link 'src' -[type]-> 'dst'>``.

        Example:
            >>> link
            <Link 'a' -[relation]-> 'b'>
        """
        return (
            f"<Link {self.source_id!r} -[{self.link_type}]-> {self.target_id!r}>"
        )