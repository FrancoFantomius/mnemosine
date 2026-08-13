"""Search: LIKE-based text search and vector k-NN.

Exposes :class:`Search` (via ``storage.search``) with a text search over the
``content``/``path``/``metadata`` columns and a vector k-NN search that
delegates to :class:`mnemosine.vec.VectorStore`.
"""

from .util import escape_like


class Search:
    def __init__(self, storage):
        """Wrap a Storage and expose search operations.

        Access a ``Search`` through ``storage.search`` rather than
        constructing it directly.

        Args:
            storage (Storage): The storage to search.

        Returns:
            Search: A search view over the storage.
        """
        self._storage = storage

    def text(self, query, kind=None, limit=100, fields=("content", "path", "metadata")):
        """Find nodes whose text fields contain ``query`` literally.

        Uses SQL ``LIKE`` with ``%``/``_`` escaped, so the query is matched
        literally rather than as a wildcard. Matches are combined with ``OR``
        across the requested fields.

        Args:
            query (str): The substring to search for.
            kind (str | None): Only return nodes of this kind.
            limit (int): Maximum number of results. Defaults to 100.
            fields (tuple of str): Columns to search: ``"content"``,
                ``"path"`` and/or ``"metadata"``.

        Returns:
            list of Node: The matching nodes, newest first (unsorted).

        Raises:
            ValueError: If ``fields`` contains an unknown column.

        Example:
            >>> db.node(kind="doc").update(title="Project Plan").save()
            >>> [n["title"] for n in db.search.text("Plan")]
            ['Project Plan']
        """
        allowed = {"content", "path", "metadata"}
        like = f"%{escape_like(query)}%"
        clauses = []
        params = []
        for field in fields:
            if field not in allowed:
                raise ValueError(f"unsupported field {field!r}, choose from {sorted(allowed)}")
            clauses.append(f"{field} LIKE ? ESCAPE '\\'")
            params.append(like)
        sql = "SELECT id FROM nodes WHERE " + " OR ".join(clauses)
        if kind:
            sql += " AND kind = ?"
            params.append(kind)
        sql += " LIMIT ?"
        params.append(limit)
        rows = self._storage.conn.execute(sql, params).fetchall()
        return [self._storage.get(r["id"]) for r in rows]

    def vector(self, vector, top_k=10, metric="cosine"):
        """k-NN over stored embeddings.

        Delegates to :meth:`mnemosine.vec.VectorStore.knn`, which uses the
        ``sqlite-vec`` virtual table when available and a brute-force scan
        otherwise.

        Args:
            vector (sequence of float): The query embedding.
            top_k (int): Number of nearest neighbours to return.
            metric (str): Distance metric: ``"cosine"`` (default), ``"l2"``
                or ``"dot"``.

        Returns:
            list of dict: Each item has ``node`` (Node) and ``distance``
            (float), ordered nearest-first.

        Raises:
            VectorError: If ``top_k < 1`` or the vector dimension conflicts
                with stored embeddings.

        Example:
            >>> db.embed_fn = lambda t: [1.0, 0.0, 0.0]
            >>> doc.add_embedding()
            >>> [r["node"].id for r in db.search.vector([1.0, 0.0, 0.0], top_k=1)]
            ['01G...']
        """
        results = self._storage.vec.knn(vector, top_k=top_k, metric=metric)
        return [
            {"node": self._storage.get(r["node_id"]), "distance": r["distance"]}
            for r in results
        ]