# Rotinas de testes associadas ao arquivo restricao-eletrica.csv do NEWAVE
from datetime import datetime
from inewave.newave.modelos.restricaoeletrica import (
    RegistroRE,
    RegistroREHorizPer,
    RegistroRELimFormPer,
)

from inewave.newave.restricaoeletrica import RestricaoEletrica

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.restricaoeletrica import (
    MockRE,
    MockREHorizPer,
    MockRELimFormPer,
    MockRestricaoEletrica,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_registro_re_restricaoeletrica():
    m: MagicMock = mock_open(read_data="".join(MockRE))
    r = RegistroRE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, "1.0ger_usit(13) + ger_usih(66)"]
    assert r.codigo_restricao == 1
    r.codigo_restricao = 5
    assert r.formula == "1.0ger_usit(13) + ger_usih(66)"
    r.formula = "Teste"


def test_registro_re_horiz_per_restricaoeletrica():
    m: MagicMock = mock_open(read_data="".join(MockREHorizPer))
    r = RegistroREHorizPer()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, datetime(2021, 1, 1), datetime(2021, 1, 1)]
    assert r.codigo_restricao == 1
    r.codigo_restricao = 2
    assert r.data_inicial == datetime(2021, 1, 1)
    r.data_inicial = datetime(2021, 2, 1)
    assert r.data_final == datetime(2021, 1, 1)
    r.data_final = datetime(2022, 11, 1)


def test_registro_rhq_lim_form_per_restricaoeletrica():
    m: MagicMock = mock_open(read_data="".join(MockRELimFormPer))
    r = RegistroRELimFormPer()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [
        1,
        datetime(2021, 1, 1),
        datetime(2021, 3, 1),
        1,
        -1.1e30,
        5000.0,
    ]
    assert r.codigo_restricao == 1
    r.codigo_restricao = 2
    assert r.data_inicial == datetime(2021, 1, 1)
    r.data_inicial = datetime(2021, 2, 1)
    assert r.data_final == datetime(2021, 3, 1)
    r.data_final = datetime(2021, 4, 1)
    assert r.limite_inferior == -1.1e30
    r.limite_inferior = 0
    assert r.limite_superior == 5000
    r.limite_superior = 0


def test_atributos_encontrados_restricaoeletrica():
    m: MagicMock = mock_open(read_data="".join(MockRestricaoEletrica))
    with patch("builtins.open", m):
        e = RestricaoEletrica.read(ARQ_TESTE)
        assert len(e.re()) > 0
        assert len(e.re_horiz_per()) > 0
        assert len(e.re_lim_form_per()) > 0


def test_eq_restricaoeletrica():
    m: MagicMock = mock_open(read_data="".join(MockRestricaoEletrica))
    with patch("builtins.open", m):
        cf1 = RestricaoEletrica.read(ARQ_TESTE)
        cf2 = RestricaoEletrica.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_restricaoeletrica():
    m: MagicMock = mock_open(read_data="".join(MockRestricaoEletrica))
    with patch("builtins.open", m):
        cf1 = RestricaoEletrica.read(ARQ_TESTE)
        cf2 = RestricaoEletrica.read(ARQ_TESTE)
        cf2.data.remove(cf1.re()[0])
        assert cf1 != cf2


def test_leitura_escrita_restricaoeletrica():
    m_leitura: MagicMock = mock_open(read_data="".join(MockRestricaoEletrica))
    with patch("builtins.open", m_leitura):
        cf1 = RestricaoEletrica.read(ARQ_TESTE)
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
        cf2 = RestricaoEletrica.read(ARQ_TESTE)
        assert cf1 == cf2
