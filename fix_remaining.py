#!/usr/bin/env python3
"""Fix all remaining mypy errors in inewave/newave/."""

from __future__ import annotations
import re
from pathlib import Path


def fix_prepara_vetor_anos(filepath: Path) -> bool:
    """Fix prepara_vetor_anos_tabela(anos) where anos: List[int] -> List[str]."""
    content = filepath.read_text()
    # Find: prepara_vetor_anos_tabela(anos)
    # Replace with: prepara_vetor_anos_tabela([str(a) for a in anos])
    new_content = re.sub(
        r"prepara_vetor_anos_tabela\(anos\)",
        "prepara_vetor_anos_tabela([str(a) for a in anos])",
        content,
    )
    if new_content != content:
        filepath.write_text(new_content)
        return True
    return False


def fix_bare_list_annotations(filepath: Path) -> bool:
    """Fix bare list/List/dict annotations in type hints."""
    content = filepath.read_text()
    original = content

    # Fix ": list\n" and ": list," and ": list]" and ": list " in annotations
    # These occur in variable declarations like: variavel: list = []
    # Replace with list[Any]
    # Pattern: ": list" followed by non-[ character
    content = re.sub(r"(:\s*)list\b(?!\[)", r"\1list[Any]", content)
    content = re.sub(r"(:\s*)List\b(?!\[)", r"\1List[Any]", content)
    content = re.sub(r"(:\s*)dict\b(?!\[)", r"\1dict[str, Any]", content)

    if content != original:
        filepath.write_text(content)
        return True
    return False


def fix_tabelacsv(filepath: Path) -> bool:
    """Fix tabelacsv.py specific issues."""
    content = filepath.read_text()
    original = content

    # Fix: dict -> dict[str, list[Any]]
    content = content.replace(
        "dados: Dict[str, List] = {c: [] for c in self.__class__.COLUMN_NAMES}",
        "dados: Dict[str, List[Any]] = {c: [] for c in self.__class__.COLUMN_NAMES}",
    )

    # Fix: _monta_df type annotation
    content = content.replace(
        "    def _monta_df(self, dados: dict) -> pd.DataFrame:",
        "    def _monta_df(self, dados: dict[str, Any]) -> pd.DataFrame:",
    )

    # Fix the return value expected issues - the read method has early returns
    # without a return value
    # "return\n" without a value inside a -> bool method
    # We need to look at the read method and add return False for early exits

    if content != original:
        filepath.write_text(content)
        return True
    return False


def fix_avl_desv_files(filepath: Path) -> bool:
    """Fix avl_desvfpha_*.py files."""
    content = filepath.read_text()
    original = content

    # Fix bare dict -> dict[str, Any]
    content = re.sub(
        r"(dados|col_values):\s*dict\b(?!\[)", r"\1: dict[str, Any]", content
    )

    if content != original:
        filepath.write_text(content)
        return True
    return False


def main() -> None:
    base = Path("inewave/newave")

    # Fix prepara_vetor_anos_tabela calls
    files_with_anos = [
        "modelos/sistema.py",
        "modelos/pmo.py",
        "modelos/patamar.py",
        "modelos/parpvaz.py",
        "modelos/parpeol.py",
        "modelos/parp.py",
        "modelos/curva.py",
    ]
    for fname in files_with_anos:
        fp = base / fname
        if fix_prepara_vetor_anos(fp):
            print(f"Fixed prepara_vetor_anos in {fp}")

    # Fix bare List/list/dict annotations
    files_with_bare = [
        "modelos/blocos/tabelacsv.py",
        "modelos/conft.py",
        "modelos/confhd.py",
        "modelos/eliminacao_cortes.py",
        "modelos/pmo.py",
        "eliminacao_cortes.py",
        "cvar.py",
        "curva.py",
        "modelos/avl_desvfpha_v_q.py",
        "modelos/avl_desvfpha_s.py",
    ]
    for fname in files_with_bare:
        fp = base / fname
        if fix_bare_list_annotations(fp):
            print(f"Fixed bare list/dict in {fp}")

    print("Done with automated fixes")


if __name__ == "__main__":
    main()
