"""Compact, time-sortable unique identifiers (ULID-style).

26 chars, Crockford base32: a 48-bit millisecond timestamp plus 80 bits of
cryptographic randomness. Time-prefixed, so rows sort by creation order.
"""

import secrets
import time

_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def _encode(value: int, bits: int) -> str:
    """Encode an integer as Crockford base32 over a fixed number of bits.

    Splits ``value`` into 5-bit groups (least significant first) and maps each
    group to a character from ``_ALPHABET``. The width is ``ceil(bits / 5)``;
    any bits above ``bits`` are silently ignored.

    Args:
        value (int): The non-negative integer to encode.
        bits (int): The total bit width the encoding should cover.

    Returns:
        str: The fixed-width Crockford base32 representation.

    Example:
        >>> from mnemosine.ids import _encode
        >>> _encode(26, 5)   # 26 == 11010 -> alphabet[26] == 'Q'
        'Q'
    """
    width = (bits + 4) // 5
    chars = []
    for i in range(width):
        shift = (width - 1 - i) * 5
        chars.append(_ALPHABET[(value >> shift) & 0x1F])
    return "".join(chars)


def ulid() -> str:
    """Return a new 26-char ULID.

    The first 10 characters encode the current Unix time in milliseconds
    (48 bits) and the remaining 16 characters encode 80 bits of randomness
    generated via the CSPRNG ``secrets`` module. Because the timestamp comes
    first, ULIDs sort lexicographically in creation order.

    Returns:
        str: A 26-character Crockford base32 ULID.

    Raises:
        NotImplementedError: If the platform's ``secrets``/``os.urandom``
            cannot provide cryptographic randomness.

    Example:
        >>> from mnemosine.ids import ulid
        >>> a, b = ulid(), ulid()
        >>> len(a) == 26 and a != b
        True
    """
    ts = int(time.time() * 1000)
    return _encode(ts, 48) + _encode(secrets.randbits(80), 80)