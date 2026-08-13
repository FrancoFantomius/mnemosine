# Module `mnemosine.file`

## Overview

The File model: binary content in the on-disk blob store, deduplicated by hash.

A :class:`File` is a :class:`~mnemosine.node.Node` with ``kind == "file"``.
Its binary content lives on disk under the storage's ``blob_root``, addressed
by its SHA-256 digest (``blobs/<prefix>/<digest>``). Content is deduplicated:
two file nodes with identical bytes share one physical blob file.

## Class File

- [File](File.md)
  - [File.__init__](File.__init__.md)
  - [File.sha256](File.sha256.md)
  - [File.size_bytes](File.size_bytes.md)
  - [File.mime_type](File.mime_type.md)
  - [File.write](File.write.md)
  - [File.write_stream](File.write_stream.md)
  - [File.open](File.open.md)
  - [File.read](File.read.md)
  - [File.text](File.text.md)
  - [File._rel_path_for](File._rel_path_for.md)
  - [File._persist](File._persist.md)
  - [File.from_row](File.from_row.md)
  - [File.__repr__](File.__repr__.md)
