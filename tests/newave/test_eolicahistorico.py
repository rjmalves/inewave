# Rotinas de testes associadas ao arquivo hist-ventos.csv do NEWAVE
from datetime import datetime
from inewave.newave.modelos.eolicahistorico import (
    RegistroEolicaHistoricoVentoHorizonte,
    RegistroEolicaHistoricoVento,
    RegistroHistoricoVentoHorizonte,
    RegistroHistoricoVento,
)

from inewave.newave.eolicahistorico import EolicaHistorico

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eolicahistorico import (
    MockRegistroEolicaHistoricoHorizonte,
    MockRegistroEolicaHistorico,
    MockRegistroHistoricoVentoHorizonte,
    MockRegistroHistoricoVento,
    MockEolicaHistorico,
)


def test_registro_eolica_historico_horizonte_eolicahistorico():

    m: MagicMock = mock_open(
        read_data="".join(MockRegistroEolicaHistoricoHorizonte)
    )
    r = RegistroEolicaHistoricoVentoHorizonte()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [datetime(1979, 1, 1), datetime(2016, 1, 1)]
    assert r.data_inicial == datetime(1979, 1, 1)
    r.data_inicial = datetime(1980, 1, 1)
    assert r.data_final == datetime(2016, 1, 1)
    r.data_final = datetime(2018, 1, 1)


def test_registro_eolica_historico_eolicahistorico():

    m: MagicMock = mock_open(read_data="".join(MockRegistroEolicaHistorico))
    r = RegistroEolicaHistoricoVento()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, datetime(1979, 1, 1), datetime(1979, 2, 1), 3.43, 1.0]
    assert r.codigo_eolica == 1
    r.codigo_eolica = 2
    assert r.data_inicial == datetime(1979, 1, 1)
    r.data_inicial = datetime(1980, 1, 1)
    assert r.data_final == datetime(1979, 2, 1)
    r.data_final = datetime(1980, 2, 1)
    assert r.velocidade == 3.43
    r.velocidade = 5.0
    assert r.direcao == 1.0
    r.direcao = 0.0


def test_registro_historico_vento_horizonte_eolicahistorico():

    m: MagicMock = mock_open(
        read_data="".join(MockRegistroHistoricoVentoHorizonte)
    )
    r = RegistroHistoricoVentoHorizonte()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [datetime(1979, 1, 1), datetime(2016, 1, 1)]
    assert r.data_inicial == datetime(1979, 1, 1)
    r.data_inicial = datetime(1980, 1, 1)
    assert r.data_final == datetime(2016, 1, 1)
    r.data_final = datetime(2018, 1, 1)


def test_registro_historico_vento_eolicahistorico():

    m: MagicMock = mock_open(read_data="".join(MockRegistroHistoricoVento))
    r = RegistroHistoricoVento()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, datetime(1979, 1, 1), datetime(1979, 2, 1), 4.05, 1.0]
    assert r.codigo_posto == 1
    r.codigo_posto = 2
    assert r.data_inicial == datetime(1979, 1, 1)
    r.data_inicial = datetime(1980, 1, 1)
    assert r.data_final == datetime(1979, 2, 1)
    r.data_final = datetime(1980, 2, 1)
    assert r.velocidade == 4.05
    r.velocidade = 5.0
    assert r.direcao == 1.0
    r.direcao = 0.0


def test_atributos_encontrados_eolicahistorico():
    m: MagicMock = mock_open(read_data="".join(MockEolicaHistorico))
    with patch("builtins.open", m):
        e = EolicaHistorico.le_arquivo("")
        assert len(e.eolica_historico_vento()) > 0


def test_eq_eolicahistorico():
    m: MagicMock = mock_open(read_data="".join(MockEolicaHistorico))
    with patch("builtins.open", m):
        cf1 = EolicaHistorico.le_arquivo("")
        cf2 = EolicaHistorico.le_arquivo("")
        assert cf1 == cf2


def test_neq_eolicahistorico():
    m: MagicMock = mock_open(read_data="".join(MockEolicaHistorico))
    with patch("builtins.open", m):
        cf1 = EolicaHistorico.le_arquivo("")
        cf2 = EolicaHistorico.le_arquivo("")
        cf2.deleta_registro(cf1.eolica_historico_vento()[0])
        assert cf1 != cf2


def test_leitura_escrita_eolicahistorico():
    m_leitura: MagicMock = mock_open(read_data="".join(MockEolicaHistorico))
    with patch("builtins.open", m_leitura):
        cf1 = EolicaHistorico.le_arquivo("")
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
        cf2 = EolicaHistorico.le_arquivo("")
        assert cf1 == cf2
