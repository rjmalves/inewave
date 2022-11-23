# Rotinas de testes associadas ao arquivo eolica-fte.csv do NEWAVE
from datetime import datetime
from inewave.newave.modelos.eolicafte import RegistroEolicaFTE, RegistroPEEFTE

from inewave.newave.eolicafte import EolicaFTE

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eolicafte import (
    MockRegistroFuncaoProducao,
    MockEolicaFTE,
    MockRegistroPEEFTE,
)


def test_registro_eolica_funcao_producao_eolicafte():

    m: MagicMock = mock_open(read_data="".join(MockRegistroFuncaoProducao))
    r = RegistroEolicaFTE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [
        1,
        datetime(2021, 1, 1),
        datetime(2030, 12, 1),
        -0.14454132,
        0.10904637,
    ]
    assert r.codigo_eolica == 1
    r.codigo_eolica = 5
    assert r.data_inicial == datetime(2021, 1, 1)
    r.data_inicial = datetime(2021, 2, 1)
    assert r.data_final == datetime(2030, 12, 1)
    r.data_final = datetime(2030, 11, 1)
    assert r.coeficiente_linear == -0.14454132
    r.coeficiente_linear = -0.5
    assert r.coeficiente_angular == 0.10904637
    r.coeficiente_angular = 0.5


def test_registro_peefte():

    m: MagicMock = mock_open(read_data="".join(MockRegistroPEEFTE))
    r = RegistroPEEFTE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [
        1,
        datetime(2021, 1, 1),
        datetime(2030, 12, 1),
        -0.14454132687670500,
        0.10904637648150100,
    ]
    assert r.codigo_pee == 1
    r.codigo_pee = 5
    assert r.data_inicial == datetime(2021, 1, 1)
    r.data_inicial = datetime(2021, 2, 1)
    assert r.data_final == datetime(2030, 12, 1)
    r.data_final = datetime(2030, 11, 1)
    assert r.coeficiente_linear == -0.14454132687670500
    r.coeficiente_linear = -0.5
    assert r.coeficiente_angular == 0.10904637648150100
    r.coeficiente_angular = 0.5


def test_atributos_encontrados_eolicafte():
    m: MagicMock = mock_open(read_data="".join(MockEolicaFTE))
    with patch("builtins.open", m):
        e = EolicaFTE.le_arquivo("")
        assert len(e.eolica_funcao_producao()) > 0


def test_eq_eolicafte():
    m: MagicMock = mock_open(read_data="".join(MockEolicaFTE))
    with patch("builtins.open", m):
        cf1 = EolicaFTE.le_arquivo("")
        cf2 = EolicaFTE.le_arquivo("")
        assert cf1 == cf2


def test_neq_eolicafte():
    m: MagicMock = mock_open(read_data="".join(MockEolicaFTE))
    with patch("builtins.open", m):
        cf1 = EolicaFTE.le_arquivo("")
        cf2 = EolicaFTE.le_arquivo("")
        cf2.deleta_registro(cf1.eolica_funcao_producao()[0])
        assert cf1 != cf2


def test_leitura_escrita_eolicafte():
    m_leitura: MagicMock = mock_open(read_data="".join(MockEolicaFTE))
    with patch("builtins.open", m_leitura):
        cf1 = EolicaFTE.le_arquivo("")
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
        cf2 = EolicaFTE.le_arquivo("")
        assert cf1 == cf2
