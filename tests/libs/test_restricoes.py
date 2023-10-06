from datetime import datetime
from inewave.libs.modelos.restricoes import (
    RegistroRE,
    RegistroREHorizPer,
    RegistroRELimFormPer,
    RegistroRHE,
    RegistroRHEHorizPer,
    RegistroRHELsLPPEarmi,
    RegistroRHQ,
    RegistroRHQHorizPer,
    RegistroRHQLsLPPVoli,
)

from inewave.libs.restricoes import Restricoes

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.restricoes import (
    MockRE,
    MockREHorizPer,
    MockRELimFormPer,
    MockRHE,
    MockRHEHorizPer,
    MockRHELsLPPEarmi,
    MockRHQ,
    MockRHQHorizPer,
    MockRHQLsLPPVoli,
    MockRestricoes,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_registro_re():
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


def test_registro_re_horiz_per():
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


def test_registro_rhq_lim_form_per():
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


def test_registro_rhe():
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


def test_registro_rhe_horiz_per():
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


def test_registro_rhe_ls_lpp_earmi():
    m: MagicMock = mock_open(read_data="".join(MockRHELsLPPEarmi))
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


def test_registro_rhq():
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


def test_registro_rhq_horiz_per():
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


def test_registro_rhq_ls_lpp_voli():
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


def test_atributos_encontrados_restricoes():
    m: MagicMock = mock_open(read_data="".join(MockRestricoes))
    with patch("builtins.open", m):
        e = Restricoes.read(ARQ_TESTE)
        assert len(e.re()) > 0
        assert len(e.re_horiz_per()) > 0
        assert len(e.re_lim_form_per()) > 0
        assert len(e.rhe()) > 0
        assert len(e.rhe_horiz_per()) > 0
        assert len(e.rhe_ls_lpp_earmi()) > 0
        assert len(e.rhq()) > 0
        assert len(e.rhq_horiz_per()) > 0
        assert len(e.rhq_ls_lpp_voli()) > 0


def test_eq_restricoes():
    m: MagicMock = mock_open(read_data="".join(MockRestricoes))
    with patch("builtins.open", m):
        cf1 = Restricoes.read(ARQ_TESTE)
        cf2 = Restricoes.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_restricoes():
    m: MagicMock = mock_open(read_data="".join(MockRestricoes))
    with patch("builtins.open", m):
        cf1 = Restricoes.read(ARQ_TESTE)
        cf2 = Restricoes.read(ARQ_TESTE)
        cf2.data.remove(cf1.re()[0])
        assert cf1 != cf2


def test_leitura_escrita_restricoes():
    m_leitura: MagicMock = mock_open(read_data="".join(MockRestricoes))
    with patch("builtins.open", m_leitura):
        cf1 = Restricoes.read(ARQ_TESTE)
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
        cf2 = Restricoes.read(ARQ_TESTE)
        assert cf1 == cf2
