# Module `mnemosine.schema`

## Overview

SQL schema for the base tables (applied by migration 001).

The statements in :data:`BASE_SCHEMA` are executed once by the first
migration. Schema evolution is handled by the migration runner in
`mnemosine.migrations`; dynamic, user-defined attributes never require a
migration because they live inside the `nodes.metadata` JSON column.

## Functions

- [_ident](_ident.md)
- [_json_path_key](_json_path_key.md)
- [index_json_attribute](index_json_attribute.md)
