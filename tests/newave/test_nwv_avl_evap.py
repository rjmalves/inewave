from inewave.newave.nwv_avl_evap import NwvAvlEvap

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.nwv_avl_evap import MockNwvAvlEvap

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_nwv_avl_evap():
    m: MagicMock = mock_open(read_data="".join(MockNwvAvlEvap))
    with patch("builtins.open", m):
        rel = NwvAvlEvap.read(ARQ_TESTE)
        assert rel.versao == "FPHA_NEWAVE"
        assert rel.tabela.at[0, "periodo"] == 1
        assert rel.tabela.at[0, "codigo_usina"] == 4
        assert rel.tabela.at[0, "nome_usina"] == "FUNIL-GRANDE"
        assert rel.tabela.at[0, "volume_armazenado_hm3"] == 265.86
        assert rel.tabela.at[0, "evaporacao_calculada_hm3"] == 0.23
        assert rel.tabela.at[0, "evaporacao_modelo_hm3"] == 0.23
        assert rel.tabela.at[0, "desvio_absoluto_hm3"] == 0.0
        assert rel.tabela.at[0, "desvio_percentual"] == 0.0


def test_eq_nwv_avl_evap():
    m: MagicMock = mock_open(read_data="".join(MockNwvAvlEvap))
    with patch("builtins.open", m):
        rel1 = NwvAvlEvap.read(ARQ_TESTE)
        rel2 = NwvAvlEvap.read(ARQ_TESTE)
        assert rel1 == rel2


def test_neq_nwv_avl_evap():
    m: MagicMock = mock_open(read_data="".join(MockNwvAvlEvap))
    with patch("builtins.open", m):
        rel1 = NwvAvlEvap.read(ARQ_TESTE)
        rel2 = NwvAvlEvap.read(ARQ_TESTE)
        rel1.tabela.iloc[0, 0] = -1
        assert rel1 != rel2
