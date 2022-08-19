from datetime import timedelta
from inewave.newave.modelos.newavetim import (
    BlocoTemposEtapasTim,
)

from inewave.newave.newavetim import NewaveTim


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.newavetim import MockBlocoTemposEtapas, MockNewaveTim


def test_tempos_etapas():

    m: MagicMock = mock_open(read_data="".join(MockBlocoTemposEtapas))
    b = BlocoTemposEtapasTim()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 5
    assert b.data.shape[1] == 2
    assert b.data.iloc[0, 0] == "Leitura de Dados"
    assert b.data.iloc[-1, -1] == timedelta(hours=3, minutes=26, seconds=7)


def test_atributos_encontrados_newavetim():
    m: MagicMock = mock_open(read_data="".join(MockNewaveTim))
    with patch("builtins.open", m):
        nt = NewaveTim.le_arquivo("")
        assert nt.tempos_etapas is not None


def test_atributos_nao_encontrados_newavetim():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        nt = NewaveTim.le_arquivo("")
        assert nt.tempos_etapas is None


def test_eq_newavetim():
    m: MagicMock = mock_open(read_data="".join(MockNewaveTim))
    with patch("builtins.open", m):
        nt1 = NewaveTim.le_arquivo("")
        nt2 = NewaveTim.le_arquivo("")
        assert nt1 == nt2


def test_neq_newavetim():
    m: MagicMock = mock_open(read_data="".join(MockNewaveTim))
    with patch("builtins.open", m):
        nt1 = NewaveTim.le_arquivo("")
        nt2 = NewaveTim.le_arquivo("")
        nt2.tempos_etapas.iloc[0, 0] = ""
        assert nt1 != nt2
