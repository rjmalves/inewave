from datetime import timedelta
from unittest.mock import MagicMock, patch

from inewave.newave.modelos.newavetim import (
    BlocoTemposEtapasTim,
    BlocoTemposIteracoesTim,
    BlocoVersaoModeloTim,
)
from inewave.newave.newavetim import Newavetim
from tests.mocks.arquivos.newavetim import (
    MockBlocoTemposEtapas,
    MockBlocoTemposIteracoes,
    MockBlocoTemposIteracoesIncompleto,
    MockBlocoVersaoModelo,
    MockNewaveTim,
)
from tests.mocks.mock_open import mock_open

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


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


def test_tempos_iteracoes():
    m: MagicMock = mock_open(read_data="".join(MockBlocoTemposIteracoes))
    b = BlocoTemposIteracoesTim()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.columns.tolist() == [
        "iteracao",
        "backward",
        "forward",
        "total",
    ]
    assert b.data["iteracao"].tolist() == [1, 2]
    # Os tempos sem sentido da primeira iteração são mantidos como escritos
    assert b.data.loc[0, "backward"] == timedelta(
        hours=110, minutes=46, seconds=23
    )
    assert b.data.loc[0, "forward"] == timedelta(
        hours=633, minutes=13, seconds=39
    )
    assert b.data.loc[0, "total"] == timedelta(seconds=2)
    assert b.data.loc[1, "backward"] == timedelta(seconds=1.5)
    assert b.data.loc[1, "total"] == timedelta(seconds=4.5)


def test_tempos_iteracoes_ignora_iteracao_incompleta():
    m: MagicMock = mock_open(
        read_data="".join(MockBlocoTemposIteracoesIncompleto)
    )
    b = BlocoTemposIteracoesTim()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data["iteracao"].tolist() == [1]


def test_versao_modelo():
    m: MagicMock = mock_open(read_data="".join(MockBlocoVersaoModelo))
    b = BlocoVersaoModeloTim()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == "28.6.3_CPAMP"


def test_atributos_encontrados_newavetim():
    m: MagicMock = mock_open(read_data="".join(MockNewaveTim))
    with patch("builtins.open", m):
        nt = Newavetim.read(ARQ_TESTE)
        assert nt.tempos_etapas is not None
        assert nt.versao_modelo is not None
        tempos = nt.tempos_iteracoes
        assert tempos is not None
        assert tempos["iteracao"].tolist() == list(range(1, 51))
        assert tempos.loc[49, "total"] == timedelta(minutes=6, seconds=25)


def test_atributos_nao_encontrados_newavetim():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        nt = Newavetim.read(ARQ_TESTE)
        assert nt.tempos_etapas is None
        assert nt.tempos_iteracoes is None
        assert nt.versao_modelo is None


def test_eq_newavetim():
    m: MagicMock = mock_open(read_data="".join(MockNewaveTim))
    with patch("builtins.open", m):
        nt1 = Newavetim.read(ARQ_TESTE)
        nt2 = Newavetim.read(ARQ_TESTE)
        assert nt1 == nt2


def test_neq_newavetim():
    m: MagicMock = mock_open(read_data="".join(MockNewaveTim))
    with patch("builtins.open", m):
        nt1 = Newavetim.read(ARQ_TESTE)
        nt2 = Newavetim.read(ARQ_TESTE)
        nt2.tempos_etapas.iloc[0, 0] = ""
        assert nt1 != nt2


# NOTE: Output-only file, round-trip test not applicable
