"""Ordered, forward-only schema migrations.

A migration is a tuple ``(version, name, fn)``. The current version is stored
in ``PRAGMA user_version``; on connect, every migration above the stored
version is applied inside its own transaction. Add new migrations to the end
of :data:`MIGRATIONS` and keep them additive-first so old databases upgrade in
place without data loss.
"""

import logging

from .schema import BASE_SCHEMA

log = logging.getLogger("mnemosine.migrations")


def _base(conn):
    """Apply the base schema (migration 001).

    Executes every statement in :data:`mnemosine.schema.BASE_SCHEMA` against
    the connection. Called only when a database's ``user_version`` is below 1.

    Args:
        conn (sqlite3.Connection): An open connection to the database.

    Returns:
        None

    Example:
        >>> from mnemosine.migrations import _base
        >>> import sqlite3
        >>> conn = sqlite3.connect(":memory:")
        >>> _base(conn)
        >>> conn.execute("SELECT name FROM sqlite_master WHERE name='nodes'").fetchone()[0]
        'nodes'
    """
    for statement in BASE_SCHEMA:
        conn.execute(statement)


MIGRATIONS = [
    (1, "base schema", _base),
]


def latest_version() -> int:
    """Return the newest schema version known to the library.

    The version is the first element of the last entry in
    :data:`MIGRATIONS`. A freshly connected database is migrated up to this
    value.

    Returns:
        int: The latest migration version.

    Example:
        >>> from mnemosine.migrations import latest_version
        >>> latest_version()
        1
    """
    return MIGRATIONS[-1][0]


def migrate(conn, target: int | None = None):
    """Apply pending migrations to ``conn``.

    Reads ``PRAGMA user_version``, then runs each migration whose version is
    greater than the stored version (and, if given, not greater than
    ``target``). Each migration runs inside its own transaction so a failure
    rolls back cleanly; the version is bumped only after the migration body
    succeeds. Idempotent: calling again after a successful run is a no-op.

    Args:
        conn (sqlite3.Connection): An open connection to the database.
        target (int | None): Optional upper bound version. Migrations above
            this value are skipped. ``None`` means "migrate to the latest".

    Returns:
        int: The schema version that was stored before migrating (the
        ``current`` value).

    Raises:
        sqlite3.Error: If any migration statement fails; the failed
            migration's transaction is rolled back first.

    Example:
        >>> from mnemosine.migrations import migrate, latest_version
        >>> import sqlite3
        >>> conn = sqlite3.connect(":memory:")
        >>> migrate(conn)
        0
        >>> conn.execute("PRAGMA user_version").fetchone()[0] == latest_version()
        True
    """
    current = conn.execute("PRAGMA user_version").fetchone()[0]
    for version, name, fn in MIGRATIONS:
        if version <= current:
            continue
        if target is not None and version > target:
            break
        conn.execute("BEGIN")
        try:
            fn(conn)
            conn.execute(f"PRAGMA user_version = {version}")
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        log.info("applied migration %d (%s)", version, name)
    return current