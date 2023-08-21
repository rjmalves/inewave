from datetime import datetime
from inewave.newave.modelos.ghmin import BlocoUHEGhmin
from inewave.newave import Ghmin

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch
from datetime import datetime
from tests.mocks.arquivos.ghmin import MockGhmin

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_uhe_ghmin():
    m: MagicMock = mock_open(read_data="".join(MockGhmin))
    b = BlocoUHEGhmin()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 110
    assert b.data.shape[1] == 4
    assert b.data.iloc[0, 0] == 275
    assert b.data.iloc[0, 1] == datetime(2020, 1, 1)
    assert b.data.iloc[0, 2] == 0
    assert b.data.iloc[0, 3] == 1215.0
    assert b.data.iloc[-1, -1] == 5943.0


def test_atributos_encontrados_ghmin():
    m: MagicMock = mock_open(read_data="".join(MockGhmin))
    with patch("builtins.open", m):
        ad = Ghmin.read(ARQ_TESTE)
        assert ad.geracoes is not None


def test_atributos_nao_encontrados_ghmin():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Ghmin.read(ARQ_TESTE)
        assert ad.geracoes is None


def test_eq_ghmin():
    m: MagicMock = mock_open(read_data="".join(MockGhmin))
    with patch("builtins.open", m):
        ad1 = Ghmin.read(ARQ_TESTE)
        ad2 = Ghmin.read(ARQ_TESTE)
        assert ad1 == ad2


def test_neq_ghmin():
    m: MagicMock = mock_open(read_data="".join(MockGhmin))
    with patch("builtins.open", m):
        ad1 = Ghmin.read(ARQ_TESTE)
        ad2 = Ghmin.read(ARQ_TESTE)
        ad2.geracoes.iloc[0, 0] = -1
        assert ad1 != ad2


def test_leitura_escrita_ghmin():
    m_leitura: MagicMock = mock_open(read_data="".join(MockGhmin))
    with patch("builtins.open", m_leitura):
        ad1 = Ghmin.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ad1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        ad2 = Ghmin.read(ARQ_TESTE)
        assert ad1 == ad2
