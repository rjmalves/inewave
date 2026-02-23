#!/usr/bin/env python3
"""Fix mypy strict errors in inewave/newave/ mechanically.

Round 2 fixes:
1. Change read/write -> None to -> bool and add return True
2. Change IO[str]/IO[bytes] in read/write overrides to IO[Any]
3. Fix remaining bare IO -> IO[Any]
4. Fix property setters -> None (missing some)
5. Fix nested __offset functions return types
"""

from __future__ import annotations
import re
from pathlib import Path


def fix_read_write_to_bool(content: str) -> str:
    """Change read/write -> None to -> bool and add return True.

    The base classes Section.read, Section.write, Block.read, Block.write
    all return bool. Our overrides must match.
    """
    # Fix: -> None: at end of read/write def -> -> bool:
    # and add return True to the body

    lines = content.split("\n")
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect read/write method def with -> None:
        m = re.match(
            r"(\s+)def (read|write)\(self,\s*file:[^)]+\)[^:]*->\s*None:",
            line,
        )
        if m:
            indent = m.group(1)
            # Replace -> None: with -> bool:
            new_line = re.sub(r"->\s*None:", "-> bool:", line)
            result.append(new_line)
            i += 1
            # Now we need to find the end of this method body and add return True
            # Collect the body lines
            method_body_start = i
            method_lines = []
            # Find the body: lines indented more than the def
            body_indent = indent + "    "
            while i < len(lines):
                body_line = lines[i]
                # Empty line or comment - include
                stripped = body_line.strip()
                if stripped == "" or stripped.startswith("#"):
                    method_lines.append(body_line)
                    i += 1
                elif body_line.startswith(body_indent):
                    method_lines.append(body_line)
                    i += 1
                else:
                    # End of method
                    break
            # Add return True before end of method (after last non-empty line)
            # Find last non-empty line index in method_lines
            last_content_idx = -1
            for j in range(len(method_lines) - 1, -1, -1):
                if method_lines[j].strip():
                    last_content_idx = j
                    break
            if last_content_idx >= 0:
                method_lines.insert(
                    last_content_idx + 1, f"{body_indent}return True"
                )
            result.extend(method_lines)
            continue
        result.append(line)
        i += 1
    return "\n".join(result)


def fix_io_any(content: str) -> str:
    """Replace IO[str] and IO[bytes] in read/write overrides with IO[Any].

    Also fix remaining bare IO -> IO[Any].
    """
    # Replace IO[str] and IO[bytes] in method signatures with IO[Any]
    content = re.sub(
        r"def (read|write)\(self,\s*file:\s*IO\[(?:str|bytes)\]",
        r"def \1(self, file: IO[Any]",
        content,
    )
    # Replace remaining bare IO (not followed by [) -> IO[Any]
    content = re.sub(r"\bIO\b(?!\[)", "IO[Any]", content)
    return content


def fix_remaining_setters(content: str) -> str:
    """Fix any property setters still missing -> None.

    The previous round may have missed some patterns.
    """
    lines = content.split("\n")
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check if this is a @X.setter line
        if re.match(r"\s*@\w+\.setter\s*$", line):
            result.append(line)
            i += 1
            # Next meaningful line should be the def
            while i < len(lines) and lines[i].strip() == "":
                result.append(lines[i])
                i += 1
            if i < len(lines):
                def_line = lines[i]
                # Add -> None if missing return type
                if (
                    re.match(r"\s*def \w+\(self,", def_line)
                    and "->" not in def_line
                    and def_line.rstrip().endswith(":")
                ):
                    def_line = re.sub(r":$", " -> None:", def_line.rstrip())
                result.append(def_line)
                i += 1
            continue
        result.append(line)
        i += 1
    return "\n".join(result)


def fix_offset_nested_functions(content: str) -> str:
    """Add return types to __offset_* nested functions."""
    lines = content.split("\n")
    result = []
    for line in lines:
        # Check for untyped nested offset functions
        if re.match(
            r"\s+def (__offset_primeiro_bloco|__offset_segundo_bloco|__inicializa_variaveis|__atualiza_registros|__converte_arrays_em_dataframes)\(\):",
            line,
        ):
            name = re.search(r"def (\w+)\(\)", line)
            if name:
                fname = name.group(1)
                if fname in (
                    "__offset_primeiro_bloco",
                    "__offset_segundo_bloco",
                ):
                    line = re.sub(r"\(\):", "() -> int:", line)
                elif fname in (
                    "__inicializa_variaveis",
                    "__atualiza_registros",
                ):
                    line = re.sub(r"\(\):", "() -> None:", line)
                elif fname == "__converte_arrays_em_dataframes":
                    line = re.sub(r"\(\):", "() -> None:", line)
        result.append(line)
    return "\n".join(result)


def fix_no_any_return_from_data(content: str) -> str:
    """Fix 'Returning Any from function declared to return X' for self.data[N].

    Properties that return self.data[N] where N is an int return Any.
    The fix is to cast: return cast(X, self.data[N])
    We need to ensure cast is imported.
    """
    # This is complex - skip for now and handle with targeted casts
    return content


def ensure_cast_import(content: str) -> str:
    """Ensure cast is imported from typing if needed."""
    if "cast(" in content and "cast" not in re.findall(
        r"from typing import ([^\n]+)", content
    ):
        match = re.search(
            r"^from typing import ([^\n]+)$", content, re.MULTILINE
        )
        if match:
            existing = match.group(1).strip()
            if "cast" not in existing:
                content = content.replace(
                    f"from typing import {existing}",
                    f"from typing import cast, {existing}",
                    1,
                )
    return content


def get_newave_py_files() -> list[Path]:
    """Get all Python files in inewave/newave/ excluding nwlistop/nwlistcf."""
    base = Path("inewave/newave")
    files = list(base.rglob("*.py"))
    files = [
        f
        for f in files
        if "nwlistop" not in str(f) and "nwlistcf" not in str(f)
    ]
    return sorted(files)


def fix_file(filepath: Path) -> bool:
    """Apply round 2 fixes. Returns True if file was modified."""
    content = filepath.read_text(encoding="utf-8")
    original = content

    content = fix_read_write_to_bool(content)
    content = fix_io_any(content)
    content = fix_remaining_setters(content)
    content = fix_offset_nested_functions(content)

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        return True
    return False


def main() -> None:
    files = get_newave_py_files()
    print(f"Round 2: Processing {len(files)} files...")

    modified = 0
    for fp in files:
        changed = fix_file(fp)
        if changed:
            modified += 1
            print(f"  Fixed: {fp}")

    print(f"\nModified {modified} files")


if __name__ == "__main__":
    main()
