# Module `mnemosine.ids`

## Overview

Compact, time-sortable unique identifiers (ULID-style).

26 chars, Crockford base32: a 48-bit millisecond timestamp plus 80 bits of
cryptographic randomness. Time-prefixed, so rows sort by creation order.

## Functions

- [_encode](_encode.md)
- [ulid](ulid.md)
