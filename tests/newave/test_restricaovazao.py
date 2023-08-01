# Rotinas de testes associadas ao arquivo restricao-vazao.csv do NEWAVE
from datetime import datetime
from inewave.newave.modelos.restricaovazao import (
    RegistroRHQ,
    RegistroRHQHorizPer,
    RegistroRHQLsLPPVoli,
)

from inewave.newave.restricaovazao import RestricaoVazao

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.restricaovazao import (
    MockRHQ,
    MockRHQHorizPer,
    MockRHQLsLPPVoli,
    MockRestricaoVazao,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_registro_rhq_restricaovazao():
    m: MagicMock = mock_open(read_data="".join(MockRHQ))
    r = RegistroRHQ()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, "qtur(66)"]
    assert r.codigo_restricao == 1
    r.codigo_restricao = 5
    assert r.formula == "qtur(66)"
    r.formula = "Teste"


def test_registro_rhq_horiz_per_restricaovazao():
    m: MagicMock = mock_open(read_data="".join(MockRHQHorizPer))
    r = RegistroRHQHorizPer()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, datetime(2021, 1, 1), datetime(2022, 12, 1)]
    assert r.codigo_restricao == 1
    r.codigo_restricao = 2
    assert r.data_inicial == datetime(2021, 1, 1)
    r.data_inicial = datetime(2021, 2, 1)
    assert r.data_final == datetime(2022, 12, 1)
    r.data_final = datetime(2022, 11, 1)


def test_registro_rhq_ls_lpp_voli_restricaovazao():
    m: MagicMock = mock_open(read_data="".join(MockRHQLsLPPVoli))
    r = RegistroRHQLsLPPVoli()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, 1, 0.3, 3000.0]
    assert r.codigo_restricao == 1
    r.codigo_restricao = 2
    assert r.indice_reta == 1
    r.indice_reta = 2
    assert r.coeficiente_angular == 0.3
    r.coeficiente_angular = 0.5
    assert r.coeficiente_linear == 3000.0
    r.coeficiente_linear = 3500.0


def test_atributos_encontrados_restricaovazao():
    m: MagicMock = mock_open(read_data="".join(MockRestricaoVazao))
    with patch("builtins.open", m):
        e = RestricaoVazao.read(ARQ_TESTE)
        assert len(e.rhq()) > 0
        assert len(e.rhq_horiz_per()) > 0
        assert len(e.rhq_ls_lpp_voli()) > 0


def test_eq_restricaovazao():
    m: MagicMock = mock_open(read_data="".join(MockRestricaoVazao))
    with patch("builtins.open", m):
        cf1 = RestricaoVazao.read(ARQ_TESTE)
        cf2 = RestricaoVazao.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_restricaovazao():
    m: MagicMock = mock_open(read_data="".join(MockRestricaoVazao))
    with patch("builtins.open", m):
        cf1 = RestricaoVazao.read(ARQ_TESTE)
        cf2 = RestricaoVazao.read(ARQ_TESTE)
        cf2.data.remove(cf1.rhq()[0])
        assert cf1 != cf2


def test_leitura_escrita_restricaovazao():
    m_leitura: MagicMock = mock_open(read_data="".join(MockRestricaoVazao))
    with patch("builtins.open", m_leitura):
        cf1 = RestricaoVazao.read(ARQ_TESTE)
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
        cf2 = RestricaoVazao.read(ARQ_TESTE)
        assert cf1 == cf2
