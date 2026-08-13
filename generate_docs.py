#!/usr/bin/env python3
"""Generate markdown documentation from module docstrings into ``docs/``.

Every function and method in the ``mnemosine`` package is documented by a
docstring in the source code. This script parses those docstrings (no
imports, using only the ``ast`` module) and writes one markdown file per
function/method/class into ``docs/<module>/`` plus a ``index.md`` overview
for each module.

Usage::

    python generate_docs.py          # regenerate everything under docs/

The docstrings follow a light convention that this script understands:

- Section headers on their own line, e.g. ``Args:``, ``Returns:``,
  ``Raises:``, ``Yields:``, ``Example:``.
- Parameter/return lines inside those sections formatted as
  ``name (type): description`` (rendered as bullet lists).
- Code examples starting with ``>>>`` (rendered as fenced ``python``
  blocks).

Any other content is treated as plain markdown paragraphs.
"""

from __future__ import annotations

import ast
import re
import shutil
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent / "mnemosine"
DOCS_DIR = Path(__file__).resolve().parent / "docs"

SECTION_HEADERS = {
    "Args",
    "Returns",
    "Raises",
    "Yields",
    "Example",
    "Examples",
    "Note",
    "Notes",
    "Warning",
    "Warnings",
    "Tip",
    "Tips",
}
_HEADER_RE = re.compile(rf"^({'|'.join(SECTION_HEADERS)}):$")


def render_docstring(doc: str | None) -> list[str]:
    """Convert a plain docstring into a list of markdown lines.

    Args:
        doc (str | None): The raw docstring (may be ``None``).

    Returns:
        list of str: Markdown lines ready to join with ``\\n``.
    """
    if not doc:
        return ["_No documentation provided._"]
    out: list[str] = []
    in_code = False
    in_section = False
    for raw in doc.split("\n"):
        line = raw.strip()

        # A section header on its own line.
        if not in_code and _HEADER_RE.match(line):
            title = line[:-1]
            out.append("")
            out.append(f"**{title}:**")
            in_section = title in ("Args", "Returns", "Raises", "Yields")
            continue

        if in_code:
            # Blank lines, indented lines and doctest prompts stay inside the
            # block (indented doctest *output* is a continuation of the code).
            if (
                line == ""
                or raw[:1] in (" ", "\t")
                or line.startswith(">>>")
                or line.startswith("...")
            ):
                out.append(line)
                continue
            # A non-indented, non-prompt line ends the block.
            out.append("```")
            in_code = False
            in_section = False
            # Fall through and process this line normally below.
        elif line.startswith(">>>") or line.startswith("..."):
            in_code = True
            out.append("")
            out.append("```python")
            out.append(line)
            continue

        if in_section:
            if line == "":
                out.append("")
                continue
            if ": " in line:
                name, _, desc = line.partition(": ")
                out.append(f"- `{name}`: {desc}")
            else:
                out.append(f"- {line}")
            continue

        out.append(line if line else "")

    if in_code:
        out.append("```")
    return out


def build_signature(fn: ast.FunctionDef) -> str:
    """Build a compact signature string from a function AST node.

    Args:
        fn (ast.FunctionDef): The function node.

    Returns:
        str: ``(args)`` or ``(args) -> return_type``.
    """
    args = ast.unparse(fn.args)
    signature = f"({args})"
    if fn.returns is not None:
        signature += f" -> {ast.unparse(fn.returns)}"
    return signature


def collect_entries(tree: ast.Module) -> list[dict]:
    """Collect class / function / method documentation entries.

    Args:
        tree (ast.Module): The parsed module.

    Returns:
        list of dict: Each entry has ``qualname``, ``kind``, ``signature``,
        ``doc`` and ``class_name`` keys.
    """
    entries: list[dict] = []

    def entry(qualname, kind, signature, doc, class_name=None):
        entries.append(
            {
                "qualname": qualname,
                "kind": kind,
                "signature": signature,
                "doc": doc,
                "class_name": class_name,
            }
        )

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            entry(
                node.name,
                "class",
                f"class {node.name}",
                ast.get_docstring(node),
            )
            for item in node.body:
                if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                kind = "method"
                prop_variant = None
                for deco in item.decorator_list:
                    if isinstance(deco, ast.Name) and deco.id == "property":
                        kind = "property"
                    elif isinstance(deco, ast.Attribute) and deco.attr in ("setter", "deleter"):
                        prop_variant = deco.attr
                if prop_variant:
                    kind = f"property-{prop_variant}"
                qualname = f"{node.name}.{item.name}"
                entry(
                    qualname,
                    kind,
                    f"{node.name}.{item.name}{build_signature(item)}",
                    ast.get_docstring(item),
                    class_name=node.name,
                )
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            entry(
                node.name,
                "function",
                f"{node.name}{build_signature(node)}",
                ast.get_docstring(node),
            )
    return entries


def module_title(module_name: str) -> str:
    """Return the display title for a module.

    Args:
        module_name (str): The docs-folder name of the module.

    Returns:
        str: ``mnemosine.<module>`` (or ``mnemosine`` for the package).
    """
    if module_name == "package":
        return "mnemosine"
    return f"mnemosine.{module_name}"


def write_function_page(out_dir: Path, entry: dict) -> None:
    """Write one markdown page per function/method/class.

    Args:
        out_dir (Path): The module's docs subfolder.
        entry (dict): A single entry from :func:`collect_entries`.

    Returns:
        None
    """
    lines = [
        f"# `{module_title(out_dir.name)}.{entry['qualname']}`",
        "",
        f"**Kind:** {entry['kind']}",
        "",
        "## Signature",
        "",
        "```python",
        entry["signature"],
        "```",
        "",
        "## Documentation",
        "",
    ]
    lines.extend(render_docstring(entry["doc"]))
    lines.append("")
    (out_dir / f"{entry['qualname']}.md").write_text("\n".join(lines), encoding="utf-8")


def append_property_variant(out_dir: Path, entry: dict) -> None:
    """Append a property setter/deleter to the property's existing page.

    Property getters, setters and deleters all share the same ``qualname``
    (e.g. ``Node.metadata``), so the setter/deleter documentation is appended
    as a subsection instead of overwriting the getter page.

    Args:
        out_dir (Path): The module's docs subfolder.
        entry (dict): A ``property-setter`` / ``property-deleter`` entry.

    Returns:
        None
    """
    page = out_dir / f"{entry['qualname']}.md"
    if not page.exists():
        write_function_page(out_dir, entry)
        return
    variant = entry["kind"].removeprefix("property-")
    lines = [
        "",
        "---",
        "",
        f"## Property {variant}",
        "",
        "```python",
        entry["signature"],
        "```",
        "",
    ]
    lines.extend(render_docstring(entry["doc"]))
    lines.append("")
    with page.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def write_module_index(out_dir: Path, module_doc: str | None, entries: list[dict]) -> None:
    """Write the ``index.md`` overview for a module.

    Args:
        out_dir (Path): The module's docs subfolder.
        module_doc (str | None): The module docstring.
        entries (list of dict): Entries collected from the module.

    Returns:
        None
    """
    lines = [
        f"# Module `{module_title(out_dir.name)}`",
        "",
        "## Overview",
        "",
    ]
    lines.extend(render_docstring(module_doc))
    lines.append("")

    functions = [e for e in entries if e["kind"] == "function"]
    if functions:
        lines.append("## Functions")
        lines.append("")
        for e in functions:
            lines.append(f"- [{e['qualname']}]({e['qualname']}.md)")
        lines.append("")

    classes = [e for e in entries if e["kind"] == "class"]
    for cls in classes:
        lines.append(f"## Class {cls['qualname']}")
        lines.append("")
        lines.append(f"- [{cls['qualname']}]({cls['qualname']}.md)")
        seen = set()
        methods = [e for e in entries if e.get("class_name") == cls["qualname"]]
        for m in methods:
            if m["qualname"] in seen:
                continue
            seen.add(m["qualname"])
            lines.append(f"  - [{m['qualname']}]({m['qualname']}.md)")
        lines.append("")

    (out_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


def generate_module(source: Path) -> tuple[str, int]:
    """Generate the docs for a single module file.

    Args:
        source (Path): A ``.py`` file inside the package.

    Returns:
        tuple[str, int]: The docs folder name and number of entries written.
    """
    if source.name == "__init__.py":
        folder = "package"
    else:
        folder = source.stem
    tree = ast.parse(source.read_text(encoding="utf-8"))
    module_doc = ast.get_docstring(tree)
    entries = collect_entries(tree)

    out_dir = DOCS_DIR / folder
    out_dir.mkdir(parents=True, exist_ok=True)
    write_module_index(out_dir, module_doc, entries)
    for entry in entries:
        if entry["kind"] in ("property-setter", "property-deleter"):
            append_property_variant(out_dir, entry)
        else:
            write_function_page(out_dir, entry)
    return folder, len(entries)


def main() -> None:
    """Regenerate the documentation tree under ``docs/``.

    Returns:
        None
    """
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True)

    total = 0
    for source in sorted(PACKAGE_DIR.glob("*.py")):
        if source.name == "generate_docs.py":
            continue
        folder, count = generate_module(source)
        total += count
        print(f"  {source.name:>16} -> docs/{folder}/  ({count} entries)")

    print(f"\nGenerated {total} documentation pages under {DOCS_DIR}")


if __name__ == "__main__":
    main()