from datetime import datetime
from inewave.newave.modelos.expt import BlocoUTEExpt
from inewave.newave import Expt

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.expt import MockExpt
import pandas as pd

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_ute_expt():
    m: MagicMock = mock_open(read_data="".join(MockExpt))
    b = BlocoUTEExpt()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 591
    assert b.data.shape[1] == 6
    assert b.data.iloc[0, 0] == 97
    assert b.data.iloc[0, 1] == "POTEF"
    assert b.data.iloc[0, 2] == 216.00
    assert b.data.iloc[0, 3] == datetime(2020, 1, 1)
    assert pd.isnull(b.data.iloc[0, 4])
    assert b.data.iloc[0, 5] == "CUBATAO"
    assert b.data.iloc[-1, -1] == "TERMOCEARA"


def test_atributos_encontrados_expt():
    m: MagicMock = mock_open(read_data="".join(MockExpt))
    with patch("builtins.open", m):
        ad = Expt.read(ARQ_TESTE)
        assert ad.expansoes is not None


def test_atributos_nao_encontrados_expt():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Expt.read(ARQ_TESTE)
        assert ad.expansoes is None


def test_eq_expt():
    m: MagicMock = mock_open(read_data="".join(MockExpt))
    with patch("builtins.open", m):
        ad1 = Expt.read(ARQ_TESTE)
        ad2 = Expt.read(ARQ_TESTE)
        assert ad1 == ad2


def test_neq_expt():
    m: MagicMock = mock_open(read_data="".join(MockExpt))
    with patch("builtins.open", m):
        ad1 = Expt.read(ARQ_TESTE)
        ad2 = Expt.read(ARQ_TESTE)
        ad2.expansoes.iloc[0, 0] = -1
        assert ad1 != ad2


def test_leitura_escrita_expt():
    m_leitura: MagicMock = mock_open(read_data="".join(MockExpt))
    with patch("builtins.open", m_leitura):
        ad1 = Expt.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ad1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        ad2 = Expt.read(ARQ_TESTE)
        assert ad1 == ad2
