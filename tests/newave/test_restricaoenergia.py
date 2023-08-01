# Rotinas de testes associadas ao arquivo restricao-energia.csv do NEWAVE
from datetime import datetime
from inewave.newave.modelos.restricaoenergia import (
    RegistroRHE,
    RegistroRHEHorizPer,
    RegistroRHELsLPPEarmi,
)

from inewave.newave.restricaoenergia import RestricaoEnergia

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.restricaoenergia import (
    MockRHE,
    MockRHEHorizPer,
    MockRHQLsLPPEarmi,
    MockRestricaoEnergia,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_registro_rhe_restricaoenergia():
    m: MagicMock = mock_open(read_data="".join(MockRHE))
    r = RegistroRHE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, "ger_ree(1) + ener_ver_ree(1)"]
    assert r.codigo_restricao == 1
    r.codigo_restricao = 5
    assert r.formula == "ger_ree(1) + ener_ver_ree(1)"
    r.formula = "Teste"


def test_registro_rhe_horiz_per_restricaoenergia():
    m: MagicMock = mock_open(read_data="".join(MockRHEHorizPer))
    r = RegistroRHEHorizPer()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [2, datetime(2021, 1, 1), datetime(2025, 12, 1)]
    assert r.codigo_restricao == 2
    r.codigo_restricao = 1
    assert r.data_inicial == datetime(2021, 1, 1)
    r.data_inicial = datetime(2021, 2, 1)
    assert r.data_final == datetime(2025, 12, 1)
    r.data_final = datetime(2025, 11, 1)


def test_registro_rhe_ls_lpp_earmi_restricaoenergia():
    m: MagicMock = mock_open(read_data="".join(MockRHQLsLPPEarmi))
    r = RegistroRHELsLPPEarmi()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [2, 2, -0.3, 4000.0]
    assert r.codigo_restricao == 2
    r.codigo_restricao = 1
    assert r.indice_reta == 2
    r.indice_reta = 1
    assert r.coeficiente_angular == -0.3
    r.coeficiente_angular = -0.5
    assert r.coeficiente_linear == 4000.0
    r.coeficiente_linear = 3500.0


def test_atributos_encontrados_restricaoenergia():
    m: MagicMock = mock_open(read_data="".join(MockRestricaoEnergia))
    with patch("builtins.open", m):
        e = RestricaoEnergia.read(ARQ_TESTE)
        assert len(e.rhe()) > 0
        assert len(e.rhe_horiz_per()) > 0
        assert len(e.rhe_ls_lpp_earmi()) > 0


def test_eq_restricaoenergia():
    m: MagicMock = mock_open(read_data="".join(MockRestricaoEnergia))
    with patch("builtins.open", m):
        cf1 = RestricaoEnergia.read(ARQ_TESTE)
        cf2 = RestricaoEnergia.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_restricaoenergia():
    m: MagicMock = mock_open(read_data="".join(MockRestricaoEnergia))
    with patch("builtins.open", m):
        cf1 = RestricaoEnergia.read(ARQ_TESTE)
        cf2 = RestricaoEnergia.read(ARQ_TESTE)
        cf2.data.remove(cf1.rhe()[0])
        assert cf1 != cf2


def test_leitura_escrita_restricaoenergia():
    m_leitura: MagicMock = mock_open(read_data="".join(MockRestricaoEnergia))
    with patch("builtins.open", m_leitura):
        cf1 = RestricaoEnergia.read(ARQ_TESTE)
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
        cf2 = RestricaoEnergia.read(ARQ_TESTE)
        assert cf1 == cf2
