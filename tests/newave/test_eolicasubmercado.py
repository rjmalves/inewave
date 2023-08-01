# Rotinas de testes associadas ao arquivo eolica-submercado.csv do NEWAVE
from inewave.newave.modelos.eolicasubmercado import (
    RegistroEolicaSubmercado,
    RegistroPEESubmercado,
)

from inewave.newave.eolicasubmercado import EolicaSubmercado

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eolicasubmercado import (
    MockRegistroEolicaSubmercado,
    MockRegistroPEESubmercado,
    MockEolicaSubmercado,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_registro_eolica_submercado_eolicasubmercado():
    m: MagicMock = mock_open(read_data="".join(MockRegistroEolicaSubmercado))
    r = RegistroEolicaSubmercado()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [5, 2]
    assert r.codigo_eolica == 5
    r.codigo_eolica = 2
    assert r.codigo_submercado == 2
    r.codigo_submercado = 1


def test_registro_pee_submercado_eolicasubmercado():
    m: MagicMock = mock_open(read_data="".join(MockRegistroPEESubmercado))
    r = RegistroPEESubmercado()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, 3]
    assert r.codigo_pee == 1
    r.codigo_pee = 2
    assert r.codigo_submercado == 3
    r.codigo_submercado = 1


def test_atributos_encontrados_eolicasubmercado():
    m: MagicMock = mock_open(read_data="".join(MockEolicaSubmercado))
    with patch("builtins.open", m):
        e = EolicaSubmercado.read(ARQ_TESTE)
        assert len(e.eolica_submercado()) > 0


def test_eq_eolicasubmercado():
    m: MagicMock = mock_open(read_data="".join(MockEolicaSubmercado))
    with patch("builtins.open", m):
        cf1 = EolicaSubmercado.read(ARQ_TESTE)
        cf2 = EolicaSubmercado.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_eolicasubmercado():
    m: MagicMock = mock_open(read_data="".join(MockEolicaSubmercado))
    with patch("builtins.open", m):
        cf1 = EolicaSubmercado.read(ARQ_TESTE)
        cf2 = EolicaSubmercado.read(ARQ_TESTE)
        cf2.data.remove(cf1.eolica_submercado()[0])
        assert cf1 != cf2


def test_leitura_escrita_eolicasubmercado():
    m_leitura: MagicMock = mock_open(read_data="".join(MockEolicaSubmercado))
    with patch("builtins.open", m_leitura):
        cf1 = EolicaSubmercado.read(ARQ_TESTE)
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
        cf2 = EolicaSubmercado.read(ARQ_TESTE)
        assert cf1 == cf2
