"""The File model: binary content in the on-disk blob store, deduplicated by hash.

A :class:`File` is a :class:`~mnemosine.node.Node` with ``kind == "file"``.
Its binary content lives on disk under the storage's ``blob_root``, addressed
by its SHA-256 digest (``blobs/<prefix>/<digest>``). Content is deduplicated:
two file nodes with identical bytes share one physical blob file.
"""

import hashlib
import io
import os
from pathlib import Path

from .exceptions import FileNotFound
from .node import Node


class File(Node):
    def __init__(self, storage, name=None, mime=None, id=None, content=None, metadata=None):
        """Create a new, unsaved file node.

        The node row is only persisted when content is written or :meth:`save`
        is called explicitly. Use :meth:`mnemosine.Storage.file` in normal
        code.

        Args:
            storage (Storage): The owning storage.
            name (str | None): Logical file name or path (stored in
                ``node.path``).
            mime (str | None): MIME type, stored under the ``"mime"``
                metadata key.
            id (str | None): Explicit node id; defaults to a fresh ULID.
            content (bytes | str | None): Initial content; ignored in favour
                of the blob store once :meth:`write` is used.
            metadata (dict | None): Extra dynamic attributes.

        Returns:
            File: A new unsaved file node.

        Example:
            >>> from mnemosine import Storage
            >>> with Storage(":memory:") as db:
            ...     f = db.file("report.pdf", mime="application/pdf")
            ...     print(f.path, f.kind, f.mime_type)
            report.pdf file application/pdf
        """
        meta = dict(metadata or {})
        if mime is not None:
            meta.setdefault("mime", mime)
        super().__init__(
            storage, id=id, kind="file", path=name, content=content, metadata=meta
        )
        self._rel_path = None
        self._sha256 = None
        self._size = None

    # ---- properties -------------------------------------------------------

    @property
    def sha256(self):
        """Hex SHA-256 digest of the stored content, or ``None``.

        Populated after :meth:`write` (or when the node is loaded from the
        database and has content).

        Returns:
            str | None: The 64-char lowercase digest.

        Example:
            >>> f.write(b"hello")
            '2cf24dba...'
            >>> f.sha256
            '2cf24dba...'
        """
        return self._sha256

    @property
    def size_bytes(self):
        """Size of the stored content in bytes, or ``None``.

        Returns:
            int | None: The content size after :meth:`write`.

        Example:
            >>> f.write(b"hello")
            >>> f.size_bytes
            5
        """
        return self._size

    @property
    def mime_type(self):
        """The MIME type of this file.

        Returns:
            str | None: The ``"mime"`` metadata value, if set.

        Example:
            >>> f = db.file("a.png", mime="image/png")
            >>> f.mime_type
            'image/png'
        """
        return self._metadata.get("mime")

    # ---- content ----------------------------------------------------------

    def write(self, data: bytes) -> str:
        """Store bytes (or text) as this file's content.

        Convenience wrapper around :meth:`write_stream`. Strings are encoded
        as UTF-8. The bytes are streamed to a temporary file, hashed, then
        atomically moved to their content-addressed location. Replaces any
        previous content.

        Args:
            data (bytes | str): The content to store.

        Returns:
            str: The SHA-256 digest of the content.

        Raises:
            BlobStoreError: If writing to the blob store fails.

        Example:
            >>> digest = f.write(b"%PDF-1.4 fake")
            >>> len(digest) == 64
            True
        """
        if isinstance(data, str):
            data = data.encode()
        return self.write_stream(io.BytesIO(data))

    def write_stream(self, fileobj, chunk_size: int = 1 << 16) -> str:
        """Stream content from a binary file object into the blob store.

        Reads ``fileobj`` in chunks of ``chunk_size`` bytes, hashing as it
        goes, so arbitrarily large files never fully load into memory. The
        data is written to a temp file first and atomically renamed to its
        final content-addressed path.

        Args:
            fileobj (BinaryIO): Any object exposing ``read(n) -> bytes``.
            chunk_size (int): Read chunk size in bytes (default 64 KiB).

        Returns:
            str: The SHA-256 digest of the streamed content.

        Raises:
            BlobStoreError: If writing to the blob store fails.

        Example:
            >>> import io
            >>> with open("big.bin", "rb") as fh:  # doctest: +SKIP
            ...     digest = file.write_stream(fh)
        """
        root = self._storage.blob_root
        tmp_dir = root / ".tmp"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        tmp = tmp_dir / f"{self.id}-{os.urandom(8).hex()}.part"
        sha = hashlib.sha256()
        size = 0
        try:
            with open(tmp, "wb") as out:
                while True:
                    block = fileobj.read(chunk_size)
                    if not block:
                        break
                    sha.update(block)
                    out.write(block)
                    size += len(block)
            digest = sha.hexdigest()
            rel = self._rel_path_for(digest)
            final = root / rel
            final.parent.mkdir(parents=True, exist_ok=True)
            if final.exists() and final.stat().st_size == size:
                tmp.unlink(missing_ok=True)
            else:
                os.replace(tmp, final)
            self._sha256 = digest
            self._size = size
            self._rel_path = rel
            self._persist()
            return digest
        finally:
            tmp.unlink(missing_ok=True)

    def open(self):
        """Open the stored content as a binary file object.

        Returns:
            BinaryIO: A file handle positioned at the start of the content.

        Raises:
            FileNotFound: If this file has no stored content or the blob file
                is missing from disk.

        Example:
            >>> with f.open() as fh:
            ...     head = fh.read(10)
        """
        if not self._rel_path:
            raise FileNotFound(self.id)
        path = self._storage.blob_root / self._rel_path
        if not path.exists():
            raise FileNotFound(self.id)
        return open(path, "rb")

    def read(self) -> bytes:
        """Return the entire stored content as bytes.

        Returns:
            bytes: The full content.

        Raises:
            FileNotFound: If the file has no stored content.

        Example:
            >>> f.write(b"hello world")
            >>> f.read()
            b'hello world'
        """
        with self.open() as fh:
            return fh.read()

    def text(self, encoding="utf-8") -> str:
        """Return the stored content decoded as text.

        Args:
            encoding (str): Text encoding to use. Defaults to UTF-8.

        Returns:
            str: The decoded content.

        Raises:
            FileNotFound: If the file has no stored content.
            UnicodeDecodeError: If the bytes are not valid in ``encoding``.

        Example:
            >>> f.write(b"hello")
            >>> f.text()
            'hello'
        """
        return self.read().decode(encoding)

    @staticmethod
    def _rel_path_for(digest: str) -> str:
        """Compute the content-addressed blob path for a digest.

        Args:
            digest (str): A 64-char hex SHA-256 digest.

        Returns:
            str: A POSIX-style relative path ``blobs/<first2>/<digest>``.

        Example:
            >>> File._rel_path_for("ab" * 32)
            'blobs/ab/abababababababababababababababababababababababababababababababab'
        """
        return (Path("blobs") / digest[:2] / digest).as_posix()

    # ---- persistence --------------------------------------------------------

    def _persist(self):
        """Write the node row and blob metadata row in one transaction.

        Called after content is stored on disk. Inserts or updates both the
        ``nodes`` row (via ``_save_row``) and the ``blobs`` row.

        Returns:
            None

        Example:
            >>> f.write(b"x")  # triggers _persist internally
        """
        with self._storage.transaction():
            self._save_row(self._storage.conn)
            self._storage.conn.execute(
                "INSERT INTO blobs (node_id, rel_path, sha256, size_bytes, mime_type) "
                "VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(node_id) DO UPDATE SET rel_path = excluded.rel_path, "
                "sha256 = excluded.sha256, size_bytes = excluded.size_bytes, "
                "mime_type = excluded.mime_type",
                (self.id, self._rel_path, self._sha256, self._size, self.mime_type),
            )

    @classmethod
    def from_row(cls, storage, row):
        """Build a File from a database row, loading its blob metadata.

        Internal helper used by :meth:`mnemosine.Storage.get`.

        Args:
            storage (Storage): The owning storage.
            row (sqlite3.Row): A row from the ``nodes`` table.

        Returns:
            File: A loaded file node.

        Example:
            >>> row = db.conn.execute("SELECT * FROM nodes").fetchone()
            >>> File.from_row(db, row)
            <File ...>
        """
        obj = super().from_row(storage, row)
        obj._rel_path = None
        obj._sha256 = None
        obj._size = None
        blob = storage.conn.execute(
            "SELECT rel_path, sha256, size_bytes, mime_type FROM blobs WHERE node_id = ?",
            (row["id"],),
        ).fetchone()
        if blob is not None:
            obj._rel_path = blob["rel_path"]
            obj._sha256 = blob["sha256"]
            obj._size = blob["size_bytes"]
            if blob["mime_type"]:
                obj._metadata["mime"] = blob["mime_type"]
        return obj

    def __repr__(self):
        """A short, readable representation of the file.

        Returns:
            str: ``<File id='...' name='...' sha256=...>``.

        Example:
            >>> f
            <File id='01G...' name='a.txt' sha256=...>
        """
        return f"<File id={self.id!r} name={self.path!r} sha256={self._sha256}>"