"""Tests for validate() with explicit version parameters.

Validates block type matching for both correct and mismatched versions.
Diagnostic fields (missing_types, unexpected_types) confirm version correctness.
"""

import warnings
from unittest.mock import MagicMock, patch

from cfinterface.versioning import VersionMatchResult

from inewave.newave.avl_cortesfpha_nwv import AvlCortesFpha
from inewave.newave.modelos.avl_cortesfpha_nwv import (
    TabelaAvlCortesFpha,
    TabelaAvlCortesFpha28,
)
from inewave.newave.modelos.blocos.versaomodelo import (
    VersaoModelo,
    VersaoModeloLibs,
)
from inewave.nwlistop.cmarg import Cmarg
from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.cmarg import CmargsAnos, CmargsAnos27
from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.pivarm import PivarmAnos, PivarmAnos_v29_2
from inewave.nwlistop.pivarm import Pivarm
from tests.mocks.arquivos.avl_cortesfpha_nwv import (
    MockAvlCortesFphaNwv,
    MockAvlCortesFphaNwv28,
)
from tests.mocks.arquivos.cmarg import MockCmarg27
from tests.mocks.arquivos.pivarm import MockPivarm
from tests.mocks.mock_open import mock_open

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_validate_cmarg_correct_version():
    """Cmarg read with version='27' validates cleanly against version '27'."""
    m: MagicMock = mock_open(read_data="".join(MockCmarg27))
    with patch("builtins.open", m):
        n = Cmarg.read(ARQ_TESTE, version="27")

    result: VersionMatchResult = n.validate(version="27")

    assert isinstance(result, VersionMatchResult)
    assert result.missing_types == []
    assert result.unexpected_types == []
    assert Submercado in result.found_types
    assert CmargsAnos27 in result.found_types


def test_validate_cmarg_mismatch_version():
    """Cmarg read with version='27' detects mismatch when validated against '29.4.1'."""
    m: MagicMock = mock_open(read_data="".join(MockCmarg27))
    with patch("builtins.open", m):
        n = Cmarg.read(ARQ_TESTE, version="27")

    result: VersionMatchResult = n.validate(version="29.4.1")

    assert isinstance(result, VersionMatchResult)
    # CmargsAnos (v29.4.1 block) was not found because data was parsed with v27
    assert CmargsAnos in result.missing_types
    # CmargsAnos27 (v27 block) should appear as unexpected for v29.4.1
    assert CmargsAnos27 in result.unexpected_types


def test_validate_pivarm_correct_version():
    """Pivarm read with version='28.12' validates cleanly against version '28.12'."""
    m: MagicMock = mock_open(read_data="".join(MockPivarm))
    with patch("builtins.open", m):
        n = Pivarm.read(ARQ_TESTE, version="28.12")

    result: VersionMatchResult = n.validate(version="28.12")

    assert isinstance(result, VersionMatchResult)
    assert result.missing_types == []
    assert result.unexpected_types == []
    assert Usina in result.found_types
    assert PivarmAnos in result.found_types


def test_validate_pivarm_mismatch_version():
    """Pivarm read with version='28.12' detects mismatch when validated against '29.2'."""
    m: MagicMock = mock_open(read_data="".join(MockPivarm))
    with patch("builtins.open", m):
        n = Pivarm.read(ARQ_TESTE, version="28.12")

    result: VersionMatchResult = n.validate(version="29.2")

    assert isinstance(result, VersionMatchResult)
    # PivarmAnos_v29_2 expected for v29.2 but data was parsed with v28.12 blocks
    assert PivarmAnos_v29_2 in result.missing_types
    # PivarmAnos (v28.12 block) is unexpected when validating against v29.2
    assert PivarmAnos in result.unexpected_types


def test_validate_avl_cortesfpha_correct_version_28():
    """AvlCortesFpha read with version='28' validates cleanly against version '28'."""
    m: MagicMock = mock_open(read_data="".join(MockAvlCortesFphaNwv28))
    with patch("builtins.open", m), warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        rel = AvlCortesFpha.read(ARQ_TESTE, version="28")

    result: VersionMatchResult = rel.validate(version="28")

    assert isinstance(result, VersionMatchResult)
    assert result.missing_types == []
    assert result.unexpected_types == []
    assert VersaoModelo in result.found_types
    assert TabelaAvlCortesFpha28 in result.found_types


def test_validate_avl_cortesfpha_mismatch_version_28_to_2816():
    """AvlCortesFpha read with version='28' detects mismatch when validated against '28.16'."""
    m: MagicMock = mock_open(read_data="".join(MockAvlCortesFphaNwv28))
    with patch("builtins.open", m), warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        rel = AvlCortesFpha.read(ARQ_TESTE, version="28")

    result: VersionMatchResult = rel.validate(version="28.16")

    assert isinstance(result, VersionMatchResult)
    # v28.16 expects VersaoModeloLibs + TabelaAvlCortesFpha; v28 data has neither
    assert TabelaAvlCortesFpha in result.missing_types
    assert VersaoModeloLibs in result.missing_types
    # v28 blocks are unexpected from v28.16's perspective
    assert TabelaAvlCortesFpha28 in result.unexpected_types
    assert VersaoModelo in result.unexpected_types


def test_validate_avl_cortesfpha_correct_version_2816():
    """AvlCortesFpha read with version='28.16' validates cleanly against version '28.16'."""
    m: MagicMock = mock_open(read_data="".join(MockAvlCortesFphaNwv))
    with patch("builtins.open", m), warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        rel = AvlCortesFpha.read(ARQ_TESTE, version="28.16")

    result: VersionMatchResult = rel.validate(version="28.16")

    assert isinstance(result, VersionMatchResult)
    assert result.missing_types == []
    assert result.unexpected_types == []
    assert VersaoModeloLibs in result.found_types
    assert TabelaAvlCortesFpha in result.found_types


def test_validate_avl_cortesfpha_mismatch_version_2816_to_28():
    """AvlCortesFpha read with version='28.16' detects mismatch when validated against '28'."""
    m: MagicMock = mock_open(read_data="".join(MockAvlCortesFphaNwv))
    with patch("builtins.open", m), warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        rel = AvlCortesFpha.read(ARQ_TESTE, version="28.16")

    result: VersionMatchResult = rel.validate(version="28")

    assert isinstance(result, VersionMatchResult)
    # v28 expects VersaoModelo + TabelaAvlCortesFpha28; v28.16 data has neither
    assert TabelaAvlCortesFpha28 in result.missing_types
    assert VersaoModelo in result.missing_types
    # v28.16 blocks are unexpected from v28's perspective
    assert TabelaAvlCortesFpha in result.unexpected_types
    assert VersaoModeloLibs in result.unexpected_types
