# Rotinas de testes associadas ao arquivo sistema.dat do NEWAVE
from inewave.newave.modelos.sistema import (
    BlocoNumeroPatamaresDeficit,
    BlocoCustosDeficit,
    BlocoIntercambioSubsistema,
    BlocoMercadoEnergiaSistema,
    BlocoGeracaoUsinasNaoSimuladas,
)

from inewave.newave import Sistema


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.sistema import (
    MockBlocoNumeroPatamaresDeficit,
    MockBlocoCustoDeficit,
    MockBlocoLimitesIntercambio,
    MockBlocoMercadoEnergia,
    MockBlocoGeracaoUsinasNaoSimuladas,
    MockSistema,
)


def test_bloco_numero_patamares_deficit_sistema():

    m: MagicMock = mock_open(
        read_data="".join(MockBlocoNumeroPatamaresDeficit)
    )
    b = BlocoNumeroPatamaresDeficit()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == 1


def test_bloco_custos_deficit_sistema():

    m: MagicMock = mock_open(read_data="".join(MockBlocoCustoDeficit))
    b = BlocoCustosDeficit()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, 0] == 11
    assert b.data.iloc[0, 3] == 6524.05


def test_bloco_limites_intercambio_sistema():

    m: MagicMock = mock_open(read_data="".join(MockBlocoLimitesIntercambio))
    b = BlocoIntercambioSubsistema()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 7500.0


def test_bloco_mercado_energia_sistema():

    m: MagicMock = mock_open(read_data="".join(MockBlocoMercadoEnergia))
    b = BlocoMercadoEnergiaSistema()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 6657.0


def test_bloco_usinas_nao_simuladas_sistema():

    m: MagicMock = mock_open(
        read_data="".join(MockBlocoGeracaoUsinasNaoSimuladas)
    )
    b = BlocoGeracaoUsinasNaoSimuladas()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 1.0


def test_atributos_encontrados_sistema():
    m: MagicMock = mock_open(read_data="".join(MockSistema))
    with patch("builtins.open", m):
        ad = Sistema.le_arquivo("")
        assert ad.numero_patamares_deficit is not None
        assert ad.custo_deficit is not None
        assert ad.limites_intercambio is not None
        assert ad.mercado_energia is not None
        assert ad.geracao_usinas_nao_simuladas is not None


def test_atributos_nao_encontrados_sistema():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Sistema.le_arquivo("")
        assert ad.numero_patamares_deficit is None
        assert ad.custo_deficit is None
        assert ad.limites_intercambio is None
        assert ad.mercado_energia is None
        assert ad.geracao_usinas_nao_simuladas is None


def test_eq_sistema():
    m: MagicMock = mock_open(read_data="".join(MockSistema))
    with patch("builtins.open", m):
        cf1 = Sistema.le_arquivo("")
        cf2 = Sistema.le_arquivo("")
        assert cf1 == cf2


def test_neq_sistema():
    m: MagicMock = mock_open(read_data="".join(MockSistema))
    with patch("builtins.open", m):
        cf1 = Sistema.le_arquivo("")
        cf2 = Sistema.le_arquivo("")
        cf2.numero_patamares_deficit = 0
        assert cf1 != cf2


def test_leitura_escrita_sistema():
    m_leitura: MagicMock = mock_open(read_data="".join(MockSistema))
    with patch("builtins.open", m_leitura):
        cf1 = Sistema.le_arquivo("")
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
        cf2 = Sistema.le_arquivo("")
        assert cf1 == cf2
