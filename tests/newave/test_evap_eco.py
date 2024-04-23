from inewave.newave.evap_eco import EvapEco

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.nwv_eco_evap import MockNwvEcoEvap

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_evap_eco():
    m: MagicMock = mock_open(read_data="".join(MockNwvEcoEvap))
    with patch("builtins.open", m):
        rel = EvapEco.read(ARQ_TESTE)
        assert rel.versao == "FPHA_NEWAVE"
        assert rel.tabela.at[0, "periodo"] == 1
        assert rel.tabela.at[0, "codigo_usina"] == 4
        assert rel.tabela.at[0, "nome_usina"] == "FUNIL-GRANDE"
        assert rel.tabela.at[0, "volume_referencia_hm3"] == 265.86
        assert rel.tabela.at[0, "evaporacao_referencia_hm3"] == 0.23
        assert rel.tabela.at[0, "coeficiente_evaporacao_mm_mes"] == 6
        assert rel.tabela.at[0, "flag_evaporacao"] == 1
        assert rel.tabela.at[0, "evaporacao_linear"] == 1
        assert rel.tabela.at[0, "tipo_volume_referencia"] == 1


def test_eq_evap_eco():
    m: MagicMock = mock_open(read_data="".join(MockNwvEcoEvap))
    with patch("builtins.open", m):
        rel1 = EvapEco.read(ARQ_TESTE)
        rel2 = EvapEco.read(ARQ_TESTE)
        assert rel1 == rel2


def test_neq_evap_eco():
    m: MagicMock = mock_open(read_data="".join(MockNwvEcoEvap))
    with patch("builtins.open", m):
        rel1 = EvapEco.read(ARQ_TESTE)
        rel2 = EvapEco.read(ARQ_TESTE)
        rel1.tabela.iloc[0, 0] = -1
        assert rel1 != rel2
