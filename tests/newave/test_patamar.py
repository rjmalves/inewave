# Rotinas de testes associadas ao arquivo patamar.dat do NEWAVE
from inewave.newave.modelos.patamar import (
    BlocoNumeroPatamares,
    BlocoDuracaoPatamar,
    BlocoCargaPatamar,
    BlocoIntercambioPatamarSubsistemas,
    BlocoUsinasNaoSimuladas,
)

from inewave.newave import Patamar


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.patamar import (
    MockBlocoNumeroPatamares,
    MockBlocoDuracaoMensalPatamares,
    MockBlocoCargaSubsistema,
    MockBlocoIntercambioSubsistemas,
    MockBlocoUsinasNaoSimuladas,
    MockPatamar,
)


def test_bloco_numero_patamares_patamar():

    m: MagicMock = mock_open(read_data="".join(MockBlocoNumeroPatamares))
    b = BlocoNumeroPatamares()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == 3


def test_bloco_duracao_patamares_patamar():

    m: MagicMock = mock_open(
        read_data="".join(MockBlocoDuracaoMensalPatamares)
    )
    b = BlocoDuracaoPatamar()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1995
    assert b.data.iloc[-1, -1] == 0.5081


def test_bloco_carga_subsistema_patamar():

    m: MagicMock = mock_open(read_data="".join(MockBlocoCargaSubsistema))
    b = BlocoCargaPatamar()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 0.9673


def test_bloco_intercambio_patamar():

    m: MagicMock = mock_open(
        read_data="".join(MockBlocoIntercambioSubsistemas)
    )
    b = BlocoIntercambioPatamarSubsistemas()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 1.0


def test_bloco_usinas_nao_simuladas_patamar():

    m: MagicMock = mock_open(read_data="".join(MockBlocoUsinasNaoSimuladas))
    b = BlocoUsinasNaoSimuladas()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 1.0


def test_atributos_encontrados_patamar():
    m: MagicMock = mock_open(read_data="".join(MockPatamar))
    with patch("builtins.open", m):
        ad = Patamar.le_arquivo("")
        assert ad.numero_patamares is not None
        assert ad.duracao_mensal_patamares is not None
        assert ad.carga_patamares is not None
        assert ad.intercambio_patamares is not None
        assert ad.usinas_nao_simuladas is not None


def test_atributos_nao_encontrados_patamar():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Patamar.le_arquivo("")
        assert ad.numero_patamares is None
        assert ad.duracao_mensal_patamares is None
        assert ad.carga_patamares is None
        assert ad.intercambio_patamares is None
        assert ad.usinas_nao_simuladas is None


def test_eq_patamar():
    m: MagicMock = mock_open(read_data="".join(MockPatamar))
    with patch("builtins.open", m):
        cf1 = Patamar.le_arquivo("")
        cf2 = Patamar.le_arquivo("")
        assert cf1 == cf2


def test_neq_patamar():
    m: MagicMock = mock_open(read_data="".join(MockPatamar))
    with patch("builtins.open", m):
        cf1 = Patamar.le_arquivo("")
        cf2 = Patamar.le_arquivo("")
        cf2.numero_patamares = 0
        assert cf1 != cf2


def test_leitura_escrita_patamar():
    m_leitura: MagicMock = mock_open(read_data="".join(MockPatamar))
    with patch("builtins.open", m_leitura):
        cf1 = Patamar.le_arquivo("")
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        cf1.escreve_arquivo("", "")
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(3, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        cf2 = Patamar.le_arquivo("")
        assert cf1 == cf2
