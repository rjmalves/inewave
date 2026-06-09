# Rotinas de testes associadas ao arquivo patamar.dat do NEWAVE
from inewave.newave.modelos.patamar import (
    BlocoNumeroPatamares,
    BlocoDuracaoPatamar,
    BlocoCargaPatamar,
    BlocoIntercambioPatamarSubsistemas,
    BlocoUsinasNaoSimuladas,
)

from inewave.newave import Patamar
from datetime import datetime
import io

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.patamar import (
    MockBlocoNumeroPatamares,
    MockBlocoDuracaoMensalPatamares,
    MockBlocoCargaSubsistema,
    MockBlocoIntercambioSubsistemas,
    MockBlocoUsinasNaoSimuladas,
    MockBlocoUsinasNaoSimuladasNomeada,
    MockPatamar,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_numero_patamares_patamar():
    m: MagicMock = mock_open(read_data="".join(MockBlocoNumeroPatamares))
    b = BlocoNumeroPatamares()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == 3


def test_bloco_duracao_patamares_patamar():
    m: MagicMock = mock_open(read_data="".join(MockBlocoDuracaoMensalPatamares))
    b = BlocoDuracaoPatamar()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == datetime(1995, 1, 1)
    assert b.data.iloc[0, 2] == 0.2366
    assert b.data.iloc[1, 2] == 0.2184
    assert b.data.iloc[2, 2] == 0.2366
    assert b.data.iloc[3, 2] == 0.2778
    assert b.data.iloc[4, 2] == 0.3226
    assert b.data.iloc[5, 2] == 0.3500
    assert b.data.iloc[6, 2] == 0.3710
    assert b.data.iloc[7, 2] == 0.3387
    assert b.data.iloc[8, 2] == 0.2917
    assert b.data.iloc[9, 2] == 0.2823
    assert b.data.iloc[10, 2] == 0.2222
    assert b.data.iloc[11, 2] == 0.2366
    assert b.data.iloc[-1, -1] == 0.5081


def test_bloco_carga_subsistema_patamar():
    m: MagicMock = mock_open(read_data="".join(MockBlocoCargaSubsistema))
    b = BlocoCargaPatamar()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[0, 1] == datetime(1995, 1, 1)
    assert b.data.iloc[0, 3] == 1.1492
    assert b.data.iloc[1, 3] == 1.1557
    assert b.data.iloc[2, 3] == 1.1522
    assert b.data.iloc[3, 3] == 1.1612
    assert b.data.iloc[4, 3] == 1.1666
    assert b.data.iloc[5, 3] == 1.1612
    assert b.data.iloc[6, 3] == 1.1530
    assert b.data.iloc[7, 3] == 1.1632
    assert b.data.iloc[8, 3] == 1.1598
    assert b.data.iloc[9, 3] == 1.1531
    assert b.data.iloc[10, 3] == 1.1623
    assert b.data.iloc[11, 3] == 1.1494
    assert b.data.iloc[-1, -1] == 0.9673


def test_bloco_intercambio_patamar():
    m: MagicMock = mock_open(read_data="".join(MockBlocoIntercambioSubsistemas))
    b = BlocoIntercambioPatamarSubsistemas()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[0, 1] == 2
    assert b.data.iloc[0, 2] == datetime(1995, 1, 1)
    assert b.data.iloc[0, 3] == 1
    assert b.data.iloc[0, 4] == 1.0000
    assert b.data.iloc[1, 4] == 1.0000
    assert b.data.iloc[2, 4] == 1.0000
    assert b.data.iloc[3, 4] == 1.0000
    assert b.data.iloc[4, 4] == 1.0000
    assert b.data.iloc[5, 4] == 1.0000
    assert b.data.iloc[6, 4] == 0.9720
    assert b.data.iloc[7, 4] == 0.9698
    assert b.data.iloc[8, 4] == 0.9688
    assert b.data.iloc[9, 4] == 0.9681
    assert b.data.iloc[10, 4] == 0.9669
    assert b.data.iloc[11, 4] == 0.9683
    assert b.data.iloc[-1, -1] == 1.0


def test_bloco_usinas_nao_simuladas_patamar():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUsinasNaoSimuladas))
    b = BlocoUsinasNaoSimuladas()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[0, 1] == 1
    assert b.data.iloc[0, 2] == ""
    assert b.data.iloc[0, 3] == datetime(1995, 1, 1)
    assert b.data.iloc[0, 4] == 1
    assert b.data.iloc[0, 5] == 1.0000
    assert b.data.iloc[1, 5] == 1.0000
    assert b.data.iloc[2, 5] == 1.0000
    assert b.data.iloc[3, 5] == 1.0000
    assert b.data.iloc[4, 5] == 1.0118
    assert b.data.iloc[5, 5] == 1.0152
    assert b.data.iloc[6, 5] == 1.0206
    assert b.data.iloc[7, 5] == 1.0222
    assert b.data.iloc[8, 5] == 1.0150
    assert b.data.iloc[9, 5] == 1.0108
    assert b.data.iloc[10, 5] == 1.0020
    assert b.data.iloc[11, 5] == 0.9965
    assert b.data.iloc[-1, -1] == 1.0


def test_bloco_usinas_nao_simuladas_cabecalho_nomeado_patamar():
    # Regressão para o issue #119: cabeçalhos de subsistema/bloco com rótulo
    # textual da fonte (p.ex. "   1   1 SUDESTE BIO", presente em decks de
    # PDE) não devem ser interpretados como linha de dados.
    m: MagicMock = mock_open(
        read_data="".join(MockBlocoUsinasNaoSimuladasNomeada)
    )
    b = BlocoUsinasNaoSimuladas()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data["valor"].isna().sum() == 0
    assert b.data["codigo_submercado"].unique().tolist() == [1, 3]
    assert sorted(b.data["indice_bloco"].unique().tolist()) == [1, 2]
    assert sorted(b.data["fonte"].unique().tolist()) == [
        "NORDESTE PCH",
        "SUDESTE BIO",
        "SUDESTE EOL",
    ]
    assert b.data["data"].min() == datetime(2024, 1, 1)
    primeiro_bio = b.data[
        (b.data["fonte"] == "SUDESTE BIO") & (b.data["patamar"] == 1)
    ]
    assert primeiro_bio["valor"].iloc[0] == 1.0

    # O rótulo da fonte deve ser preservado na escrita (round-trip).
    saida = io.StringIO()
    b.write(saida)
    b2 = BlocoUsinasNaoSimuladas()
    b2.read(io.StringIO(saida.getvalue()))
    assert b == b2


def test_atributos_encontrados_patamar():
    m: MagicMock = mock_open(read_data="".join(MockPatamar))
    with patch("builtins.open", m):
        ad = Patamar.read(ARQ_TESTE)
        assert ad.numero_patamares is not None
        assert ad.duracao_mensal_patamares is not None
        assert ad.carga_patamares is not None
        assert ad.intercambio_patamares is not None
        assert ad.usinas_nao_simuladas is not None


def test_atributos_nao_encontrados_patamar():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Patamar.read(ARQ_TESTE)
        assert ad.numero_patamares is None
        assert ad.duracao_mensal_patamares is None
        assert ad.carga_patamares is None
        assert ad.intercambio_patamares is None
        assert ad.usinas_nao_simuladas is None


def test_eq_patamar():
    m: MagicMock = mock_open(read_data="".join(MockPatamar))
    with patch("builtins.open", m):
        cf1 = Patamar.read(ARQ_TESTE)
        cf2 = Patamar.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_patamar():
    m: MagicMock = mock_open(read_data="".join(MockPatamar))
    with patch("builtins.open", m):
        cf1 = Patamar.read(ARQ_TESTE)
        cf2 = Patamar.read(ARQ_TESTE)
        cf2.numero_patamares = 0
        assert cf1 != cf2


def test_leitura_escrita_patamar():
    m_leitura: MagicMock = mock_open(read_data="".join(MockPatamar))
    with patch("builtins.open", m_leitura):
        cf1 = Patamar.read(ARQ_TESTE)
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
        cf2 = Patamar.read(ARQ_TESTE)
        # A comparação é robusta à ordem das linhas (ver __eq__ dos blocos),
        # de modo que a escrita determinística não exige reordenação manual.
        assert cf1 == cf2
