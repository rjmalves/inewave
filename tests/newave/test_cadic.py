from inewave.newave.modelos.cadic import BlocoCargasAdicionais

from inewave.newave import CAdic


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.cadic import MockBlocoCargasAdicionais


def test_bloco_ute_cadic():

    m: MagicMock = mock_open(read_data="".join(MockBlocoCargasAdicionais))
    b = BlocoCargasAdicionais()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 12
    assert b.data.shape[1] == 16
    assert b.data.iloc[0, 2] == "CONS.ITAIPU"
    assert b.data.iloc[-1, -1] == 2246


def test_atributos_encontrados_cadic():
    m: MagicMock = mock_open(read_data="".join(MockBlocoCargasAdicionais))
    with patch("builtins.open", m):
        ad = CAdic.le_arquivo("")
        assert ad.cargas is not None


def test_atributos_nao_encontrados_cadic():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = CAdic.le_arquivo("")
        assert ad.cargas is None


def test_eq_cadic():
    m: MagicMock = mock_open(read_data="".join(MockBlocoCargasAdicionais))
    with patch("builtins.open", m):
        ad1 = CAdic.le_arquivo("")
        ad2 = CAdic.le_arquivo("")
        assert ad1 == ad2


def test_neq_cadic():
    m: MagicMock = mock_open(read_data="".join(MockBlocoCargasAdicionais))
    with patch("builtins.open", m):
        ad1 = CAdic.le_arquivo("")
        ad2 = CAdic.le_arquivo("")
        ad2.cargas.iloc[0, 0] = -1
        assert ad1 != ad2


def test_leitura_escrita_cadic():
    m_leitura: MagicMock = mock_open(
        read_data="".join(MockBlocoCargasAdicionais)
    )
    with patch("builtins.open", m_leitura):
        ad1 = CAdic.le_arquivo("")
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ad1.escreve_arquivo("", "")
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(2, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        ad2 = CAdic.le_arquivo("")
        assert ad1 == ad2
