#!/usr/bin/env python3
"""Clean up all gitignored files and directories in the repository.

Usage::

    python clean.py             # Remove all gitignored files & directories
    python clean.py --dry-run   # Preview what will be removed (-n)
    python clean.py --force     # Force deletion without confirmation (-f)
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def remove_path(path: Path) -> None:
    """Remove a file or directory safely."""
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
    elif path.is_dir():
        shutil.rmtree(path, ignore_errors=True)


def clean_via_git(dry_run: bool = False, force: bool = False) -> int:
    """Use Git to identify and clean ignored files."""
    cmd = ["git", "clean", "-Xdf"]
    if dry_run:
        cmd = ["git", "clean", "-n", "-Xdf"]
    elif not force:
        # Check what will be deleted first
        preview = subprocess.run(
            ["git", "clean", "-n", "-Xdf"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if preview.returncode != 0:
            print(f"Error checking ignored files: {preview.stderr}", file=sys.stderr)
            return preview.returncode
        
        output = preview.stdout.strip()
        if not output:
            print("Nothing to clean. Working tree is already clean of ignored files.")
            return 0
        
        print("The following ignored files/directories will be removed:")
        print(output)
        confirm = input("\nProceed with deletion? [y/N]: ").strip().lower()
        if confirm not in ("y", "yes"):
            print("Aborted.")
            return 0

    res = subprocess.run(cmd, cwd=REPO_ROOT)
    return res.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove all files and directories matching .gitignore rules."
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show what would be removed without actually deleting anything.",
    )
    parser.add_argument(
        "-f",
        "-y",
        "--force",
        "--yes",
        action="store_true",
        help="Remove files directly without interactive confirmation.",
    )

    args = parser.parse_args()
    return clean_via_git(dry_run=args.dry_run, force=args.force)


if __name__ == "__main__":
    sys.exit(main())
