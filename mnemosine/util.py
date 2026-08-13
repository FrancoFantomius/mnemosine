"""Small shared helpers.

Utilities used across the mnemosine package for timestamps, JSON
serialization, and SQL ``LIKE`` escaping.
"""

import json
from datetime import datetime, timezone


def utcnow() -> str:
    """Return the current UTC time as an ISO-8601 string.

    Seconds precision, e.g. ``2026-08-13T12:34:56+00:00``. Used as the
    ``created_at`` / ``updated_at`` values on nodes and links.

    Returns:
        str: The current UTC time formatted as ISO-8601 with seconds precision.

    Example:
        >>> from mnemosine.util import utcnow
        >>> utcnow()
        '2026-08-13T12:34:56+00:00'
    """
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def dumps(value) -> str:
    """Serialize a Python value to a compact JSON string.

    Uses ``ensure_ascii=False`` so non-ASCII text is kept readable, and
    compact separators so the stored metadata stays small.

    Args:
        value (object): Any JSON-serializable value (dict, list, str, int, ...).

    Returns:
        str: The compact JSON representation of ``value``.

    Raises:
        TypeError: If ``value`` is not JSON-serializable.

    Example:
        >>> from mnemosine.util import dumps
        >>> dumps({"title": "città", "n": 1})
        '{"title":"città","n":1}'
    """
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def loads(text):
    """Parse a JSON string back into a Python value.

    Empty or ``None`` input is treated as an empty mapping, which is the
    convention used for the ``metadata`` columns.

    Args:
        text (str | None): The JSON string to parse.

    Returns:
        object: The decoded value; an empty ``dict`` when ``text`` is empty
        or ``None``.

    Raises:
        json.JSONDecodeError: If ``text`` is not valid JSON.

    Example:
        >>> from mnemosine.util import loads
        >>> loads('{"a": 1}')
        {'a': 1}
        >>> loads(None)
        {}
    """
    if not text:
        return {}
    return json.loads(text)


def escape_like(term: str) -> str:
    """Escape ``LIKE`` wildcards so user input matches literally.

    SQL's ``LIKE`` treats ``%`` and ``_`` as wildcards and ``\\`` as the
    escape character. This function escapes all three so a query such as
    ``"100%"`` matches the literal text ``100%`` instead of everything
    starting with ``100``. The SQL must use ``ESCAPE '\\'``.

    Args:
        term (str): The raw user-supplied search term.

    Returns:
        str: The same term with ``\\``, ``%`` and ``_`` escaped.

    Example:
        >>> from mnemosine.util import escape_like
        >>> escape_like("100%_done")
        '100\\\\%\\\\_done'
    """
    return term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")