from inewave.newave.nwv_cortes_evap import NwvCortesEvap

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.nwv_cortes_evap import MockNwvCortesEvap


def test_atributos_encontrados_nwv_cortes_evap():
    m: MagicMock = mock_open(read_data="".join(MockNwvCortesEvap))
    with patch("builtins.open", m):
        rel = NwvCortesEvap.le_arquivo("")
        assert rel.versao == "FPHA_NEWAVE"
        assert rel.tabela.at[0, "periodo"] == 1
        assert rel.tabela.at[0, "indice_usina"] == 4
        assert rel.tabela.at[0, "nome_usina"] == "FUNIL-GRANDE"
        assert rel.tabela.at[0, "derivada_cota_area"] == 0.0000000000
        assert rel.tabela.at[0, "derivada_volume_cota"] == 0.0000000000
        assert rel.tabela.at[0, "volume_referencia_hm3"] == 265.86
        assert rel.tabela.at[0, "evaporacao_referencia_hm3"] == 0.23
        assert rel.tabela.at[0, "coeficiente_volume"] == 0.0000000000
        assert rel.tabela.at[0, "rhs_volume"] == 0.2263


def test_eq_nwv_cortes_evap():
    m: MagicMock = mock_open(read_data="".join(MockNwvCortesEvap))
    with patch("builtins.open", m):
        rel1 = NwvCortesEvap.le_arquivo("")
        rel2 = NwvCortesEvap.le_arquivo("")
        assert rel1 == rel2


def test_neq_nwv_cortes_evap():
    m: MagicMock = mock_open(read_data="".join(MockNwvCortesEvap))
    with patch("builtins.open", m):
        rel1 = NwvCortesEvap.le_arquivo("")
        rel2 = NwvCortesEvap.le_arquivo("")
        rel1.tabela.iloc[0, 0] = -1
        assert rel1 != rel2
