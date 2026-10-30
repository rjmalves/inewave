# Rotinas de testes associadas ao arquivo vazpast.dat do NEWAVE
from inewave.newave.modelos.vazpast import BlocoVazPast

from inewave.newave import Vazpast


import io
import warnings

import pytest

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.vazpast import MockBlocoVazoesPassadas

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_desvios_vazpast():
    m: MagicMock = mock_open(read_data="".join(MockBlocoVazoesPassadas))
    b = BlocoVazPast()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 2604
    assert b.data.columns.tolist() == [
        "codigo_posto",
        "nome_posto",
        "mes",
        "valor",
        "codigo_usina",
        "nome_usina",
    ]
    assert b.data.iloc[0, 0] == 1
    assert b.data["valor"].iloc[-1] == 20.0
    # As colunas descontinuadas repetem as novas.
    assert b.data["codigo_usina"].equals(b.data["codigo_posto"])
    assert b.data["nome_usina"].equals(b.data["nome_posto"])


def test_atributos_encontrados_vazpast():
    m: MagicMock = mock_open(read_data="".join(MockBlocoVazoesPassadas))
    with patch("builtins.open", m):
        ad = Vazpast.read(ARQ_TESTE)
        assert ad.tendencia is not None


def test_atributos_nao_encontrados_vazpast():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Vazpast.read(ARQ_TESTE)
        assert ad.tendencia is None


def test_eq_vazpast():
    m: MagicMock = mock_open(read_data="".join(MockBlocoVazoesPassadas))
    with patch("builtins.open", m):
        cf1 = Vazpast.read(ARQ_TESTE)
        cf2 = Vazpast.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_vazpast():
    m: MagicMock = mock_open(read_data="".join(MockBlocoVazoesPassadas))
    with patch("builtins.open", m):
        cf1 = Vazpast.read(ARQ_TESTE)
        cf2 = Vazpast.read(ARQ_TESTE)
        cf2.tendencia.iloc[0, 0] = -1
        assert cf1 != cf2


def test_leitura_escrita_vazpast():
    m_leitura: MagicMock = mock_open(read_data="".join(MockBlocoVazoesPassadas))
    with patch("builtins.open", m_leitura):
        cf1 = Vazpast.read(ARQ_TESTE)
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
        cf2 = Vazpast.read(ARQ_TESTE)
        assert cf1 == cf2


def _le_bloco_vazpast() -> BlocoVazPast:
    b = BlocoVazPast()
    b.read(io.StringIO("".join(MockBlocoVazoesPassadas)))
    return b


def _escreve_bloco_vazpast(b: BlocoVazPast) -> str:
    buf = io.StringIO()
    b.write(buf)
    return buf.getvalue()


def test_escrita_vazpast_so_com_colunas_novas():
    b = _le_bloco_vazpast()
    original = _escreve_bloco_vazpast(b)
    b.data = b.data.drop(columns=["codigo_usina", "nome_usina"])
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        assert _escreve_bloco_vazpast(b) == original
    assert original == "".join(MockBlocoVazoesPassadas)


def test_escrita_vazpast_so_com_colunas_descontinuadas_avisa():
    b = _le_bloco_vazpast()
    original = _escreve_bloco_vazpast(b)
    b.data = b.data.drop(columns=["codigo_posto", "nome_posto"])
    with pytest.warns(DeprecationWarning, match="codigo_usina"):
        assert _escreve_bloco_vazpast(b) == original


def test_escrita_vazpast_recusa_colunas_divergentes():
    b = _le_bloco_vazpast()
    b.data.loc[b.data["codigo_usina"] == 1, "codigo_usina"] = 999
    with pytest.raises(ValueError, match="codigo_posto e codigo_usina"):
        _escreve_bloco_vazpast(b)
