# Rotinas de testes associadas ao arquivo manutt.dat do NEWAVE
from inewave.newave.modelos.manutt import BlocoManutencaoUTE

from inewave.newave import Manutt


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.manutt import MockManutt

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_uhe_manutt():
    m: MagicMock = mock_open(read_data="".join(MockManutt))
    b = BlocoManutencaoUTE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 236
    assert b.data.iloc[0, 0] == 13
    assert b.data.iloc[-1, -1] == 211.65


def test_atributos_encontrados_manutt():
    m: MagicMock = mock_open(read_data="".join(MockManutt))
    with patch("builtins.open", m):
        ad = Manutt.read(ARQ_TESTE)
        assert ad.manutencoes is not None


def test_atributos_nao_encontrados_manutt():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Manutt.read(ARQ_TESTE)
        assert ad.manutencoes is None


def test_eq_manutt():
    m: MagicMock = mock_open(read_data="".join(MockManutt))
    with patch("builtins.open", m):
        cf1 = Manutt.read(ARQ_TESTE)
        cf2 = Manutt.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_manutt():
    m: MagicMock = mock_open(read_data="".join(MockManutt))
    with patch("builtins.open", m):
        cf1 = Manutt.read(ARQ_TESTE)
        cf2 = Manutt.read(ARQ_TESTE)
        cf2.manutencoes.iloc[0, 0] = -1
        assert cf1 != cf2


def test_leitura_escrita_manutt():
    m_leitura: MagicMock = mock_open(read_data="".join(MockManutt))
    with patch("builtins.open", m_leitura):
        cf1 = Manutt.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        cf1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        cf2 = Manutt.read(ARQ_TESTE)
        assert cf1 == cf2
