"""SQL schema for the base tables (applied by migration 001).

The statements in :data:`BASE_SCHEMA` are executed once by the first
migration. Schema evolution is handled by the migration runner in
:mod:`mnemosine.migrations`; dynamic, user-defined attributes never require a
migration because they live inside the ``nodes.metadata`` JSON column.
"""

import re

BASE_SCHEMA = [
    """
    CREATE TABLE nodes (
        id         TEXT PRIMARY KEY,
        kind       TEXT NOT NULL,
        path       TEXT,
        content    TEXT,
        metadata   TEXT NOT NULL DEFAULT '{}',
        embedding  INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE node_links (
        source_id TEXT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
        target_id TEXT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
        link_type TEXT NOT NULL,
        metadata  TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        PRIMARY KEY (source_id, target_id, link_type)
    )
    """,
    """
    CREATE TABLE blobs (
        node_id    TEXT PRIMARY KEY REFERENCES nodes(id) ON DELETE CASCADE,
        rel_path   TEXT NOT NULL,
        sha256     TEXT NOT NULL,
        size_bytes INTEGER NOT NULL,
        mime_type  TEXT
    )
    """,
    "CREATE INDEX idx_nodes_kind ON nodes(kind)",
    "CREATE INDEX idx_nodes_updated ON nodes(updated_at)",
    "CREATE INDEX idx_links_source ON node_links(source_id)",
    "CREATE INDEX idx_links_target ON node_links(target_id)",
    "CREATE INDEX idx_links_type ON node_links(link_type)",
    "CREATE INDEX idx_blobs_sha256 ON blobs(sha256)",
]

_SQL_TYPES = {"TEXT", "INTEGER", "REAL", "BLOB"}


def _ident(name: str) -> str:
    """Derive a safe SQL identifier from an arbitrary metadata attribute name.

    Replaces every character outside ``[A-Za-z0-9_]`` with an underscore and
    prefixes the result with ``_`` when it would start with a digit.

    Args:
        name (str): The raw attribute name (e.g. ``"my attr"``).

    Returns:
        str: A valid SQL identifier.

    Raises:
        ValueError: If ``name`` contains no usable characters at all.

    Example:
        >>> from mnemosine.schema import _ident
        >>> _ident("my attr")
        'my_attr'
    """
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", name)
    if not cleaned:
        raise ValueError(f"cannot derive a column name from {name!r}")
    if cleaned[0].isdigit():
        cleaned = "_" + cleaned
    return cleaned


def _json_path_key(key: str) -> str:
    """Build a JSON path expression for a metadata key.

    Simple identifiers become ``$.key``; keys with spaces or special
    characters become the quoted form ``$."my key"`` with ``"`` and ``\\``
    escaped, which ``json_extract`` understands.

    Args:
        key (str): The JSON object key.

    Returns:
        str: A path expression usable by ``json_extract(metadata, <path>)``.

    Example:
        >>> from mnemosine.schema import _json_path_key
        >>> _json_path_key("title")
        '$.title'
        >>> _json_path_key("my key")
        '$."my key"'
    """
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
        return "$." + key
    escaped = key.replace("\\", "\\\\").replace('"', '\\"')
    return '$."' + escaped + '"'


def index_json_attribute(conn, attr: str, as_type: str = "TEXT") -> str:
    """Materialize a metadata JSON attribute as a generated column plus index.

    Adds a ``VIRTUAL`` generated column to ``nodes`` that extracts
    ``metadata.attr`` (using ``json_extract``) and creates an index on it, so
    ``WHERE metadata->'attr' = ...`` style queries can use the index. Safe to
    call repeatedly: existing columns and indexes are left untouched.

    Args:
        conn (sqlite3.Connection): An open connection to the database.
        attr (str): The metadata attribute to index.
        as_type (str): SQL type for the column: ``TEXT``, ``INTEGER``,
            ``REAL`` or ``BLOB``. Defaults to ``TEXT``.

    Returns:
        str: The name of the generated column (``<attr>_gen``).

    Raises:
        ValueError: If ``as_type`` is not one of ``TEXT``/``INTEGER``/
            ``REAL``/``BLOB``.

    Example:
        >>> from mnemosine import Storage
        >>> with Storage(":memory:") as db:
        ...     db.node(kind="doc").update(n=1).save()
        ...     db.node(kind="doc").update(n=2).save()
        ...     col = db.index_attribute("n", as_type="INTEGER")
        ...     db.conn.execute(f"SELECT count(*) FROM nodes WHERE {col} > 1").fetchone()[0]
        1
    """
    if as_type.upper() not in _SQL_TYPES:
        raise ValueError(f"unsupported type {as_type!r}, choose from {sorted(_SQL_TYPES)}")
    col = _ident(attr) + "_gen"
    existing = {r[1] for r in conn.execute("PRAGMA table_info(nodes)").fetchall()}
    if col not in existing:
        conn.execute(
            f"ALTER TABLE nodes ADD COLUMN {col} {as_type} "
            f"GENERATED ALWAYS AS (json_extract(metadata, '{_json_path_key(attr)}')) VIRTUAL"
        )
    conn.execute(
        f"CREATE INDEX IF NOT EXISTS idx_nodes_{_ident(attr)}_gen ON nodes({col})"
    )
    return col