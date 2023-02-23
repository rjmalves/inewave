from inewave.newave.nwv_eco_evap import NwvEcoEvap

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.nwv_eco_evap import MockNwvEcoEvap


def test_atributos_encontrados_nwv_eco_evap():
    m: MagicMock = mock_open(read_data="".join(MockNwvEcoEvap))
    with patch("builtins.open", m):
        rel = NwvEcoEvap.le_arquivo("")
        assert rel.versao == "FPHA_NEWAVE"
        assert rel.tabela.at[0, "periodo"] == 1
        assert rel.tabela.at[0, "indice_usina"] == 4
        assert rel.tabela.at[0, "nome_usina"] == "FUNIL-GRANDE"
        assert rel.tabela.at[0, "volume_referencia_hm3"] == 265.86
        assert rel.tabela.at[0, "evaporacao_referencia_hm3"] == 0.23
        assert rel.tabela.at[0, "coeficiente_evaporacao_mm_mes"] == 6
        assert rel.tabela.at[0, "flag_evaporacao"] == 1
        assert rel.tabela.at[0, "evaporacao_linear"] == 1
        assert rel.tabela.at[0, "tipo_volume_referencia"] == 1


def test_eq_nwv_eco_evap():
    m: MagicMock = mock_open(read_data="".join(MockNwvEcoEvap))
    with patch("builtins.open", m):
        rel1 = NwvEcoEvap.le_arquivo("")
        rel2 = NwvEcoEvap.le_arquivo("")
        assert rel1 == rel2


def test_neq_nwv_eco_evap():
    m: MagicMock = mock_open(read_data="".join(MockNwvEcoEvap))
    with patch("builtins.open", m):
        rel1 = NwvEcoEvap.le_arquivo("")
        rel2 = NwvEcoEvap.le_arquivo("")
        rel1.tabela.iloc[0, 0] = -1
        assert rel1 != rel2
