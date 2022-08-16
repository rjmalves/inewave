# Rotinas de testes associadas ao arquivo eolica-geracao.csv do NEWAVE
from datetime import datetime
from inewave.newave.modelos.eolicageracao import (
    RegistroEolicaGeracaoPatamar,
)

from inewave.newave.eolicageracao import EolicaGeracao

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eolicageracao import (
    MockRegistroEolicaGeracaoPatamar,
    MockEolicaGeracao,
)


def test_registro_eolica_geracao_patamar_eolicageracao():

    m: MagicMock = mock_open(
        read_data="".join(MockRegistroEolicaGeracaoPatamar)
    )
    r = RegistroEolicaGeracaoPatamar()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, datetime(2021, 1, 1), datetime(2021, 1, 1), 2, 1.0496]
    assert r.codigo_eolica == 1
    r.codigo_eolica = 2
    assert r.data_inicial == datetime(2021, 1, 1)
    r.data_inicial = datetime(2022, 1, 1)
    assert r.data_final == datetime(2021, 1, 1)
    r.data_final = datetime(2022, 1, 1)
    assert r.indice_patamar == 2
    r.indice_patamar = 1
    assert r.profundidade == 1.0496
    r.profundidade = 2.0


def test_atributos_encontrados_eolicageracao():
    m: MagicMock = mock_open(read_data="".join(MockEolicaGeracao))
    with patch("builtins.open", m):
        e = EolicaGeracao.le_arquivo("")
        assert len(e.eolica_geracao_profundidade_periodo_patamar()) > 0


def test_eq_eolicageracao():
    m: MagicMock = mock_open(read_data="".join(MockEolicaGeracao))
    with patch("builtins.open", m):
        cf1 = EolicaGeracao.le_arquivo("")
        cf2 = EolicaGeracao.le_arquivo("")
        assert cf1 == cf2


def test_neq_eolicageracao():
    m: MagicMock = mock_open(read_data="".join(MockEolicaGeracao))
    with patch("builtins.open", m):
        cf1 = EolicaGeracao.le_arquivo("")
        cf2 = EolicaGeracao.le_arquivo("")
        cf2.deleta_registro(
            cf1.eolica_geracao_profundidade_periodo_patamar()[0]
        )
        assert cf1 != cf2


def test_leitura_escrita_eolicageracao():
    m_leitura: MagicMock = mock_open(read_data="".join(MockEolicaGeracao))
    with patch("builtins.open", m_leitura):
        cf1 = EolicaGeracao.le_arquivo("")
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
        cf2 = EolicaGeracao.le_arquivo("")
        assert cf1 == cf2
