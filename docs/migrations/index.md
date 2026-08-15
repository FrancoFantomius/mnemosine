# Module `mnemosine.migrations`

## Overview

Ordered, forward-only schema migrations.

A migration is a tuple `(version, name, fn)`. The current version is stored
in `PRAGMA user_version`; on connect, every migration above the stored
version is applied inside its own transaction. Add new migrations to the end
of :data:`MIGRATIONS` and keep them additive-first so old databases upgrade in
place without data loss.

## Functions

- [_base](_base.md)
- [latest_version](latest_version.md)
- [migrate](migrate.md)
