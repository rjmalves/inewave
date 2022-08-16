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
    assert b.data.iloc[0, 1] == 0.2366
    assert b.data.iloc[0, 2] == 0.2184
    assert b.data.iloc[0, 3] == 0.2366
    assert b.data.iloc[0, 4] == 0.2778
    assert b.data.iloc[0, 5] == 0.3226
    assert b.data.iloc[0, 6] == 0.3500
    assert b.data.iloc[0, 7] == 0.3710
    assert b.data.iloc[0, 8] == 0.3387
    assert b.data.iloc[0, 9] == 0.2917
    assert b.data.iloc[0, 10] == 0.2823
    assert b.data.iloc[0, 11] == 0.2222
    assert b.data.iloc[0, 12] == 0.2366
    assert b.data.iloc[-1, -1] == 0.5081


def test_bloco_carga_subsistema_patamar():

    m: MagicMock = mock_open(read_data="".join(MockBlocoCargaSubsistema))
    b = BlocoCargaPatamar()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[0, 1] == 1995
    assert b.data.iloc[0, 2] == 1.1492
    assert b.data.iloc[0, 3] == 1.1557
    assert b.data.iloc[0, 4] == 1.1522
    assert b.data.iloc[0, 5] == 1.1612
    assert b.data.iloc[0, 6] == 1.1666
    assert b.data.iloc[0, 7] == 1.1612
    assert b.data.iloc[0, 8] == 1.1530
    assert b.data.iloc[0, 9] == 1.1632
    assert b.data.iloc[0, 10] == 1.1598
    assert b.data.iloc[0, 11] == 1.1531
    assert b.data.iloc[0, 12] == 1.1623
    assert b.data.iloc[0, 13] == 1.1494
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
    assert b.data.iloc[0, 1] == 2
    assert b.data.iloc[0, 2] == 1995
    assert b.data.iloc[0, 3] == 1.0000
    assert b.data.iloc[0, 4] == 1.0000
    assert b.data.iloc[0, 5] == 1.0000
    assert b.data.iloc[0, 6] == 1.0000
    assert b.data.iloc[0, 7] == 1.0000
    assert b.data.iloc[0, 8] == 1.0000
    assert b.data.iloc[0, 9] == 0.9720
    assert b.data.iloc[0, 10] == 0.9698
    assert b.data.iloc[0, 11] == 0.9688
    assert b.data.iloc[0, 12] == 0.9681
    assert b.data.iloc[0, 13] == 0.9669
    assert b.data.iloc[0, 14] == 0.9683
    assert b.data.iloc[-1, -1] == 1.0


def test_bloco_usinas_nao_simuladas_patamar():

    m: MagicMock = mock_open(read_data="".join(MockBlocoUsinasNaoSimuladas))
    b = BlocoUsinasNaoSimuladas()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[0, 1] == 1
    assert b.data.iloc[0, 2] == 1995
    assert b.data.iloc[0, 3] == 1.0000
    assert b.data.iloc[0, 4] == 1.0000
    assert b.data.iloc[0, 5] == 1.0000
    assert b.data.iloc[0, 6] == 1.0000
    assert b.data.iloc[0, 7] == 1.0118
    assert b.data.iloc[0, 8] == 1.0152
    assert b.data.iloc[0, 9] == 1.0206
    assert b.data.iloc[0, 10] == 1.0222
    assert b.data.iloc[0, 11] == 1.0150
    assert b.data.iloc[0, 12] == 1.0108
    assert b.data.iloc[0, 13] == 1.0020
    assert b.data.iloc[0, 14] == 0.9965
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
            chamadas[i].args[0] for i in range(2, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        cf2 = Patamar.le_arquivo("")
        assert cf1 == cf2
