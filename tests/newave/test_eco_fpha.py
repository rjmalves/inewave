from inewave.newave.eco_fpha import EcoFpha

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eco_fpha import MockEcoFpha

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_eco_fpha():
    m: MagicMock = mock_open(read_data="".join(MockEcoFpha))
    with patch("builtins.open", m):
        rel = EcoFpha.read(ARQ_TESTE)
        assert rel.versao == "FPHA_NEWAVE"
        assert rel.tabela.at[0, "codigo_usina"] == 4
        assert rel.tabela.at[0, "periodo"] == 1
        assert rel.tabela.at[0, "nome_usina"] == "FUNIL-GRANDE"
        assert rel.tabela.at[0, "tipo"] == 2
        assert rel.tabela.at[0, "conv"] == 1
        assert rel.tabela.at[0, "alfa"] == 1
        assert rel.tabela.at[0, "rems"] == 1
        assert rel.tabela.at[0, "numero_pontos_vazao_turbinada"] == 5
        assert rel.tabela.at[0, "vazao_turbinada_minima"] == 0.0
        assert rel.tabela.at[0, "vazao_turbinada_maxima"] == 507.2
        assert rel.tabela.at[0, "numero_pontos_volume_armazenado"] == 1
        assert rel.tabela.at[0, "volume_armazenado_minimo"] == 265.9
        assert rel.tabela.at[0, "volume_armazenado_maximo"] == 265.9
        assert rel.tabela.at[0, "geracao_minima"] == 0.0
        assert rel.tabela.at[0, "geracao_maxima"] == 180.0


def test_eq_eco_fpha():
    m: MagicMock = mock_open(read_data="".join(MockEcoFpha))
    with patch("builtins.open", m):
        rel1 = EcoFpha.read(ARQ_TESTE)
        rel2 = EcoFpha.read(ARQ_TESTE)
        assert rel1 == rel2


def test_neq_eco_fpha():
    m: MagicMock = mock_open(read_data="".join(MockEcoFpha))
    with patch("builtins.open", m):
        rel1 = EcoFpha.read(ARQ_TESTE)
        rel2 = EcoFpha.read(ARQ_TESTE)
        rel1.tabela.iloc[0, 0] = -1
        assert rel1 != rel2
