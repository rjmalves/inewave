# Rotinas de testes associadas ao arquivo hist-ventos.csv do NEWAVE
from datetime import datetime
from inewave.newave.modelos.eolicaposto import (
    RegistroPostoVentoCadastro,
    RegistroPEEPostoVento,
)

from inewave.newave.eolicaposto import EolicaPosto

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eolicaposto import (
    MockRegistroPostoCadastro,
    MockRegistroPEEPosto,
    MockEolicaPosto,
)


def test_registro_posto_cadastro_eolicaposto():

    m: MagicMock = mock_open(read_data="".join(MockRegistroPostoCadastro))
    r = RegistroPostoVentoCadastro()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, "NEInterior"]
    assert r.codigo_posto == 1
    r.codigo_posto = 1
    assert r.nome_posto == "NEInterior"
    r.nome_posto = "NEInterior"


def test_registro_pee_posto_eolicaposto():

    m: MagicMock = mock_open(read_data="".join(MockRegistroPEEPosto))
    r = RegistroPEEPostoVento()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, 1]
    assert r.codigo_posto == 1
    r.codigo_posto = 2
    assert r.codigo_pee == 1
    r.codigo_pee = 2


def test_atributos_encontrados_eolicaposto():
    m: MagicMock = mock_open(read_data="".join(MockEolicaPosto))
    with patch("builtins.open", m):
        e = EolicaPosto.le_arquivo("")
        assert len(e.posto_vento_cad()) > 0
        assert len(e.pee_posto()) > 0


def test_eq_eolicaposto():
    m: MagicMock = mock_open(read_data="".join(MockEolicaPosto))
    with patch("builtins.open", m):
        cf1 = EolicaPosto.le_arquivo("")
        cf2 = EolicaPosto.le_arquivo("")
        assert cf1 == cf2


def test_neq_eolicaposto():
    m: MagicMock = mock_open(read_data="".join(MockEolicaPosto))
    with patch("builtins.open", m):
        cf1 = EolicaPosto.le_arquivo("")
        cf2 = EolicaPosto.le_arquivo("")
        cf2.deleta_registro(cf1.posto_vento_cad()[0])
        assert cf1 != cf2


def test_leitura_escrita_eolicaposto():
    m_leitura: MagicMock = mock_open(read_data="".join(MockEolicaPosto))
    with patch("builtins.open", m_leitura):
        cf1 = EolicaPosto.le_arquivo("")
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
        cf2 = EolicaPosto.le_arquivo("")
        assert cf1 == cf2
