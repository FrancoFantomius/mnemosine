"""The Node model: a schema-less document with JSON metadata.

A node is the core entity of mnemosine. It always has an ``id`` and a
``kind``, plus a JSON ``metadata`` dictionary that can hold any attributes
without any schema migration. Optional ``path`` and ``content`` fields cover
text documents; binary content is handled by the :class:`~mnemosine.file.File`
subclass.
"""

from .ids import ulid
from .util import dumps, loads, utcnow


class Node:
    def __init__(
        self,
        storage,
        id=None,
        kind="text",
        path=None,
        content=None,
        metadata=None,
    ):
        """Create a new, unsaved node.

        Constructing a node does not touch the database; call :meth:`save` to
        persist it. In normal usage you do not instantiate this directly -
        use :meth:`mnemosine.Storage.node` instead.

        Args:
            storage (Storage): The storage the node belongs to.
            id (str | None): Explicit node id. Defaults to a fresh ULID.
            kind (str): Coarse type discriminator (``"text"``, ``"doc"``,
                ``"file"``, or any custom value). Defaults to ``"text"``.
            path (str | None): Optional logical name or path for the node.
            content (str | None): Optional text content stored in a dedicated
                column.
            metadata (dict | None): Initial dynamic attributes.

        Returns:
            Node: A new unsaved node instance.

        Example:
            >>> from mnemosine import Storage
            >>> with Storage(":memory:") as db:
            ...     doc = db.node(kind="doc", path="notes/hello")
            ...     doc["title"] = "Hello"
            ...     doc.save()
            ...     print(doc.id, doc.kind, doc.path)
            01G... doc notes/hello
        """
        self._storage = storage
        self.id = id or ulid()
        self.kind = kind
        self.path = path
        self.content = content
        self._metadata = dict(metadata or {})
        self._created_at = None
        self._updated_at = None
        self._saved = False

    # ---- dynamic attribute access --------------------------------------

    def __getitem__(self, key):
        """Read a dynamic attribute from the node's metadata.

        Args:
            key (str): The attribute name.

        Returns:
            object: The stored value.

        Raises:
            KeyError: If ``key`` is not present in the metadata.

        Example:
            >>> doc["title"]
            'Hello'
        """
        return self._metadata[key]

    def __setitem__(self, key, value):
        """Write a dynamic attribute into the node's metadata.

        Does not persist until :meth:`save` is called.

        Args:
            key (str): The attribute name.
            value (object): Any JSON-serializable value.

        Returns:
            None

        Example:
            >>> doc["tags"] = ["a", "b"]
        """
        self._metadata[key] = value

    def __delitem__(self, key):
        """Remove a dynamic attribute from the node's metadata.

        Args:
            key (str): The attribute name.

        Raises:
            KeyError: If ``key`` is not present in the metadata.

        Example:
            >>> del doc["title"]
        """
        del self._metadata[key]

    def __contains__(self, key):
        """Return whether the metadata holds ``key``.

        Args:
            key (str): The attribute name.

        Returns:
            bool: ``True`` if ``key`` is present in the metadata.

        Example:
            >>> "title" in doc
            True
        """
        return key in self._metadata

    def get(self, key, default=None):
        """Read a dynamic attribute without raising when missing.

        Args:
            key (str): The attribute name.
            default (object): Value returned when ``key`` is absent. Defaults
                to ``None``.

        Returns:
            object: The stored value or ``default``.

        Example:
            >>> doc.get("title", "untitled")
            'Hello'
            >>> doc.get("missing", "untitled")
            'untitled'
        """
        return self._metadata.get(key, default)

    def update(self, **values):
        """Set several dynamic attributes at once.

        Merges ``values`` into the metadata. Returns ``self`` so calls can be
        chained. Persist with :meth:`save`.

        Args:
            **values: Arbitrary keyword arguments stored as attributes. Note
                that ``content=...`` goes into the JSON metadata, not the
                ``content`` column - assign :attr:`content` directly for that.

        Returns:
            Node: This node, for chaining.

        Example:
            >>> doc.update(title="Plan", done=False).save()
        """
        self._metadata.update(values)
        return self

    @property
    def metadata(self):
        """The dynamic attribute dictionary.

        Mutating the returned dict (or replacing it) changes the node; persist
        with :meth:`save`.

        Returns:
            dict: A live reference to the node's metadata.

        Example:
            >>> doc.metadata["title"] = "Renamed"
            >>> doc.save()
        """
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        """Replace the entire metadata dictionary.

        Args:
            value (dict | None): New metadata. ``None`` becomes an empty dict.

        Example:
            >>> doc.metadata = {"title": "New"}
        """
        self._metadata = dict(value or {})

    @property
    def created_at(self):
        """Creation timestamp (ISO-8601 UTC), ``None`` until saved.

        Returns:
            str | None: The creation timestamp after the first :meth:`save`.

        Example:
            >>> doc.save()
            >>> doc.created_at
            '2026-08-13T12:34:56+00:00'
        """
        return self._created_at

    @property
    def updated_at(self):
        """Last modification timestamp (ISO-8601 UTC).

        Bumped on every :meth:`save`.

        Returns:
            str | None: The last update timestamp, or ``None`` before the
            first save.

        Example:
            >>> doc.save()
            >>> doc.updated_at
            '2026-08-13T12:34:56+00:00'
        """
        return self._updated_at

    # ---- persistence ----------------------------------------------------

    def save(self):
        """Persist this node to the database.

        Inserts a new row on first call, or updates the existing row on
        subsequent calls. Wrapped in a transaction; when called inside an
        outer :meth:`mnemosine.Storage.transaction`, it joins that
        transaction instead.

        Returns:
            Node: This node, for chaining.

        Raises:
            sqlite3.Error: If the database write fails.

        Example:
            >>> doc = db.node(kind="doc")
            >>> doc["title"] = "Hello"
            >>> doc.save()          # doctest: +SKIP
            <Node id='01G...' kind='doc'>
        """
        self._storage._save_node(self)
        return self

    def delete(self):
        """Delete this node from the database.

        Also removes its links (via ``ON DELETE CASCADE``), blob metadata row
        and any stored embedding. Blob files on disk are left for
        :meth:`mnemosine.Storage.gc_blobs`.

        Returns:
            None

        Example:
            >>> doc.delete()
        """
        self._storage._delete_node(self.id)
        self._saved = False

    def refresh(self):
        """Reload the node's fields from the database.

        Discards local, unsaved changes and re-reads ``path``, ``content``,
        metadata and timestamps.

        Returns:
            Node: This node, with fresh values.

        Raises:
            NodeNotFound: If the node no longer exists.

        Example:
            >>> doc["title"] = "unsaved change"
            >>> doc.refresh()
            >>> doc.get("title")
            'Saved value'
        """
        fresh = self._storage.get(self.id)
        self.path = fresh.path
        self.content = fresh.content
        self._metadata = dict(fresh._metadata)
        self._created_at = fresh._created_at
        self._updated_at = fresh._updated_at
        self._saved = True
        return self

    # ---- links & graph ---------------------------------------------------

    def neighbors(self, link_type=None, direction="both"):
        """Return the nodes directly connected to this node.

        Delegates to :meth:`mnemosine.Graph.neighbors`.

        Args:
            link_type (str | None): Only consider links of this type.
            direction (str): ``"out"``, ``"in"`` or ``"both"``.

        Returns:
            list of dict: Each item has ``node`` (a Node), ``link_type``
            (str) and ``metadata`` (dict).

        Example:
            >>> for item in doc.neighbors(link_type="attachment"):
            ...     print(item["node"].id, item["link_type"])
            ... # doctest: +SKIP
        """
        return self._storage.graph.neighbors(
            self, link_type=link_type, direction=direction
        )

    def links(self, direction="both", link_type=None):
        """Return the Link objects incident to this node.

        Args:
            direction (str): ``"out"`` (this node is source), ``"in"`` (this
                node is target) or ``"both"``.
            link_type (str | None): Only links of this type.

        Returns:
            list of Link: The matching links.

        Example:
            >>> for link in doc.links(direction="out"):
            ...     print(link.target_id, link.link_type)
            ... # doctest: +SKIP
        """
        return self._storage._links_for(
            self.id, direction=direction, link_type=link_type
        )

    def link(self, target, link_type="link", metadata=None):
        """Create a link from this node to ``target``.

        Convenience wrapper around :meth:`mnemosine.Storage.link`. Idempotent:
        re-linking the same pair and type returns the existing link.

        Args:
            target (Node | str): The target node, or its id.
            link_type (str): The link type. Defaults to ``"link"``.
            metadata (dict | None): Arbitrary JSON-serializable link data.

        Returns:
            Link: The created (or existing) link.

        Example:
            >>> doc.link(attachment, link_type="attachment", metadata={"v": 1})
            <Link ...>
        """
        return self._storage.link(self, target, link_type=link_type, metadata=metadata)

    def unlink(self, target, link_type="link"):
        """Remove a link between this node and ``target``.

        Args:
            target (Node | str): The target node, or its id.
            link_type (str): The link type to remove.

        Returns:
            None

        Example:
            >>> doc.unlink(attachment, link_type="attachment")
        """
        self._storage.unlink(self, target, link_type=link_type)

    # ---- embeddings -------------------------------------------------------

    def add_embedding(self, text=None):
        """Embed this node and store the vector.

        Requires ``storage.embed_fn`` to be set. When ``text`` is omitted the
        node's ``content`` is used.

        Args:
            text (str | None): Text to embed. Defaults to ``self.content``.

        Returns:
            list of float: The computed embedding vector.

        Raises:
            EmbeddingRequired: If no ``embed_fn`` is configured or there is
                no text to embed.
            VectorError: If the embedding function returns an invalid vector.

        Example:
            >>> db.embed_fn = lambda t: [1.0, 0.0]  # any embedder
            >>> doc.add_embedding()
            [1.0, 0.0]
        """
        return self._storage.embed(self, text)

    # ---- model helpers ----------------------------------------------------

    @classmethod
    def from_row(cls, storage, row):
        """Build a node from a database row.

        Internal helper used by :meth:`mnemosine.Storage.get`. Do not call
        directly.

        Args:
            storage (Storage): The owning storage.
            row (sqlite3.Row): A row from the ``nodes`` table.

        Returns:
            Node: A loaded node (subclass for ``kind == "file"``).

        Example:
            >>> row = db.conn.execute("SELECT * FROM nodes").fetchone()
            >>> Node.from_row(db, row)
            <Node ...>
        """
        obj = cls.__new__(cls)
        obj._storage = storage
        obj.id = row["id"]
        obj.kind = row["kind"]
        obj.path = row["path"]
        obj.content = row["content"]
        obj._metadata = loads(row["metadata"])
        obj._created_at = row["created_at"]
        obj._updated_at = row["updated_at"]
        obj._saved = True
        return obj

    def _save_row(self, conn):
        """Insert or update this node's row in ``conn``.

        Internal: called from within a transaction by ``storage._save_node``.

        Args:
            conn (sqlite3.Connection): The connection to write through.

        Returns:
            None

        Example:
            >>> db._save_node(doc)  # indirect usage
        """
        now = utcnow()
        if self._saved:
            conn.execute(
                "UPDATE nodes SET kind = ?, path = ?, content = ?, metadata = ?, "
                "updated_at = ? WHERE id = ?",
                (self.kind, self.path, self.content, dumps(self._metadata), now, self.id),
            )
            self._updated_at = now
        else:
            self._created_at = now
            self._updated_at = now
            conn.execute(
                "INSERT INTO nodes (id, kind, path, content, metadata, embedding, "
                "created_at, updated_at) VALUES (?, ?, ?, ?, ?, 0, ?, ?)",
                (
                    self.id,
                    self.kind,
                    self.path,
                    self.content,
                    dumps(self._metadata),
                    self._created_at,
                    self._updated_at,
                ),
            )
            self._saved = True

    def __repr__(self):
        """A short, readable representation of the node.

        Returns:
            str: ``<Node id='...' kind='...'>``.

        Example:
            >>> doc
            <Node id='01G...' kind='doc'>
        """
        return f"<Node id={self.id!r} kind={self.kind!r}>"

    def __eq__(self, other):
        """Two nodes are equal when they share the same id.

        Args:
            other (object): Any object.

        Returns:
            bool: ``True`` if ``other`` is a Node with the same id.

        Example:
            >>> doc == db.get(doc.id)
            True
        """
        return isinstance(other, Node) and other.id == self.id

    def __hash__(self):
        """Hash nodes by their id so they work in sets and dict keys.

        Returns:
            int: ``hash(self.id)``.

        Example:
            >>> {doc}  # doctest: +SKIP
            {<Node ...>}
        """
        return hash(self.id)