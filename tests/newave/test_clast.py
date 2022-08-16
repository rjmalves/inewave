# Rotinas de testes associadas ao arquivo clast.dat do NEWAVE
from inewave.newave.modelos.clast import BlocoUTEClasT
from inewave.newave.modelos.clast import BlocoModificacaoUTEClasT

from inewave.newave import ClasT


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.clast import MockBlocoUTEClasT
from tests.mocks.arquivos.clast import MockBlocoModificacaoClasT
from tests.mocks.arquivos.clast import MockClasT


def test_bloco_ute_clast():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUTEClasT))
    b = BlocoUTEClasT()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 0.0


def test_atributos_encontrados_ute_clast():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUTEClasT))
    with patch("builtins.open", m):
        ct = ClasT.le_arquivo("")
        assert ct.usinas is not None


def test_atributos_nao_encontrados_ute_clast():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ct = ClasT.le_arquivo("")
        assert ct.usinas is None


def test_bloco_modificacao_clast():
    m: MagicMock = mock_open(read_data="".join(MockBlocoModificacaoClasT))
    b = BlocoModificacaoUTEClasT()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 211
    assert b.data.iloc[-1, -1] == "PORTO ITAQUI"


def test_atributos_encontrados_modificacao_clast():
    m: MagicMock = mock_open(read_data="".join(MockClasT))
    with patch("builtins.open", m):
        ct = ClasT.le_arquivo("")
        assert ct.modificacoes is not None


def test_atributos_nao_encontrados_modificacao_clast():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ct = ClasT.le_arquivo("")
        assert ct.modificacoes is None


def test_eq_clast():
    m: MagicMock = mock_open(read_data="".join(MockClasT))
    with patch("builtins.open", m):
        ct1 = ClasT.le_arquivo("")
        ct2 = ClasT.le_arquivo("")
        assert ct1 == ct2


def test_neq_cadic():
    m: MagicMock = mock_open(read_data="".join(MockClasT))
    with patch("builtins.open", m):
        ct1 = ClasT.le_arquivo("")
        ct2 = ClasT.le_arquivo("")
        ct2.usinas.iloc[0, 0] = -1
        assert ct1 != ct2


def test_leitura_escrita_clast():
    m_leitura: MagicMock = mock_open(read_data="".join(MockClasT))
    with patch("builtins.open", m_leitura):
        ct1 = ClasT.le_arquivo("")
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ct1.escreve_arquivo("", "")
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(2, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        ct2 = ClasT.le_arquivo("")
        assert ct1 == ct2
