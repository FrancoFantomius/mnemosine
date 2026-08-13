"""Graph traversal over node_links using recursive CTEs and BFS.

The links between nodes form an undirected graph (each link connects two
nodes; direction is a property of the link, traversal can go either way).
This module provides neighbor lookup, breadth-first subgraph expansion via a
``WITH RECURSIVE`` query, and shortest-path search.
"""

from collections import deque

from .node import Node
from .util import loads


def _as_id(obj):
    """Resolve a Node instance or id string to an id.

    Args:
        obj (Node | str): A node or its id.

    Returns:
        str: The node id.

    Example:
        >>> from mnemosine.graph import _as_id
        >>> _as_id("abc")
        'abc'
    """
    return obj.id if isinstance(obj, Node) else str(obj)


class Graph:
    def __init__(self, storage):
        """Wrap a Storage and expose graph operations.

        Access a ``Graph`` through ``storage.graph`` rather than constructing
        it directly.

        Args:
            storage (Storage): The storage whose links are traversed.

        Returns:
            Graph: A graph view over the storage.
        """
        self._storage = storage

    def neighbors(self, node, link_type=None, direction="both"):
        """Return the nodes directly connected to ``node``.

        Args:
            node (Node | str): The node (or id) to inspect.
            link_type (str | None): Only follow links of this type.
            direction (str): ``"out"`` (node is the link source), ``"in"``
                (node is the link target) or ``"both"``.

        Returns:
            list of dict: Each item contains ``node`` (Node), ``link_type``
            (str) and ``metadata`` (dict).

        Raises:
            ValueError: If ``direction`` is not ``"out"``, ``"in"`` or
                ``"both"``.

        Example:
            >>> db.link(a, b, "friend")
            >>> db.link(c, a, "parent")
            >>> [n["node"].id for n in db.graph.neighbors(a, direction="both")]
            ['b', 'c']
        """
        node_id = _as_id(node)
        if direction not in ("out", "in", "both"):
            raise ValueError("direction must be 'out', 'in' or 'both'")
        arms = []
        params = []
        if direction in ("out", "both"):
            cond = "source_id = ?"
            params.append(node_id)
            if link_type:
                cond += " AND link_type = ?"
                params.append(link_type)
            arms.append(
                f"SELECT target_id AS other_id, link_type, metadata "
                f"FROM node_links WHERE {cond}"
            )
        if direction in ("in", "both"):
            cond = "target_id = ?"
            params.append(node_id)
            if link_type:
                cond += " AND link_type = ?"
                params.append(link_type)
            arms.append(
                f"SELECT source_id AS other_id, link_type, metadata "
                f"FROM node_links WHERE {cond}"
            )
        rows = self._storage.conn.execute(" UNION ALL ".join(arms), params).fetchall()
        return [
            {
                "node": self._storage.get(r["other_id"]),
                "link_type": r["link_type"],
                "metadata": loads(r["metadata"]),
            }
            for r in rows
        ]

    def subgraph(self, node, max_depth=1, link_type=None):
        """Return every node reachable from ``node`` within ``max_depth`` hops.

        Uses a ``WITH RECURSIVE`` CTE; cycle-safe because the recursion depth
        is bounded and rows are deduplicated with ``UNION``.

        Args:
            node (Node | str): The starting node (or id).
            max_depth (int): Maximum number of link hops.
            link_type (str | None): Only traverse links of this type.

        Returns:
            list of dict: Each item has ``node`` (Node) and ``depth`` (int),
            ordered by depth.

        Example:
            >>> db.link(a, b); db.link(b, c)
            >>> [(r["node"].id, r["depth"]) for r in db.graph.subgraph(a, max_depth=2)]
            [('a', 0), ('b', 1), ('c', 2)]
        """
        node_id = _as_id(node)
        sql = """
        WITH RECURSIVE reach(id, depth) AS (
            SELECT ?, 0
            UNION
            SELECT CASE WHEN l.source_id = r.id THEN l.target_id ELSE l.source_id END,
                   r.depth + 1
            FROM reach r
            JOIN node_links l ON l.source_id = r.id OR l.target_id = r.id
            WHERE r.depth < ?
        """
        params = [node_id, max_depth]
        if link_type:
            sql += " AND l.link_type = ?"
            params.append(link_type)
        sql += """
        )
        SELECT id, MIN(depth) AS depth FROM reach GROUP BY id ORDER BY depth
        """
        rows = self._storage.conn.execute(sql, params).fetchall()
        return [
            {"node": self._storage.get(r["id"]), "depth": r["depth"]} for r in rows
        ]

    def reachable(self, node, max_depth=100):
        """Return all nodes reachable from ``node`` (alias of ``subgraph``).

        Args:
            node (Node | str): The starting node (or id).
            max_depth (int): Maximum hops. Defaults to 100.

        Returns:
            list of dict: The same shape as :meth:`subgraph`.

        Example:
            >>> db.graph.reachable(a, max_depth=10)
            [{'node': <Node ...>, 'depth': 0}, ...]
        """
        return self.subgraph(node, max_depth=max_depth)

    def path(self, start, target, max_depth=100):
        """Find the shortest undirected path between two nodes via BFS.

        Returns ``None`` when no path exists within ``max_depth``. The route
        includes both endpoints, in order.

        Args:
            start (Node | str): The starting node (or id).
            target (Node | str): The target node (or id).
            max_depth (int): Maximum number of hops to explore.

        Returns:
            list of Node | None: The shortest route from ``start`` to
            ``target`` (inclusive), or ``None`` if unreachable.

        Example:
            >>> db.link(a, b); db.link(b, c)
            >>> [n.id for n in db.graph.path(a, c)]
            ['a', 'b', 'c']
            >>> db.graph.path(a, d)
            None
        """
        start_id = _as_id(start)
        target_id = _as_id(target)
        if start_id == target_id:
            return [self._storage.get(start_id)]
        visited = {start_id}
        prev = {start_id: None}
        queue = deque([start_id])
        while queue and len(visited) <= max_depth:
            current = queue.popleft()
            if current == target_id:
                break
            for other in self._neighbor_ids(current):
                if other not in visited:
                    visited.add(other)
                    prev[other] = current
                    queue.append(other)
        if target_id not in prev:
            return None
        route = []
        cursor = target_id
        while cursor is not None:
            route.append(self._storage.get(cursor))
            cursor = prev[cursor]
        route.reverse()
        return route

    def _neighbor_ids(self, node_id, link_type=None):
        """Return the ids of nodes directly connected to ``node_id``.

        Internal BFS helper; works in both link directions.

        Args:
            node_id (str): The node id.
            link_type (str | None): Optional type filter.

        Returns:
            list of str: Connected node ids (deduplicated).

        Example:
            >>> db.graph._neighbor_ids(a.id)
            ['b', 'c']
        """
        clauses = []
        params = []
        if link_type:
            clauses.append(
                "SELECT source_id AS id FROM node_links "
                "WHERE target_id = ? AND link_type = ?"
            )
            clauses.append(
                "SELECT target_id AS id FROM node_links "
                "WHERE source_id = ? AND link_type = ?"
            )
            params = [node_id, link_type, node_id, link_type]
        else:
            clauses.append("SELECT source_id AS id FROM node_links WHERE target_id = ?")
            clauses.append("SELECT target_id AS id FROM node_links WHERE source_id = ?")
            params = [node_id, node_id]
        rows = self._storage.conn.execute(" UNION ".join(clauses), params).fetchall()
        return [r["id"] for r in rows]