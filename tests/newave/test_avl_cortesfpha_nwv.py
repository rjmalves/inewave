from inewave.newave.avl_cortesfpha_nwv import AvlCortesFpha

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.avl_cortesfpha_nwv import MockAvlCortesFphaNwv

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_avl_nwv_cortesfpha_nwv():
    m: MagicMock = mock_open(read_data="".join(MockAvlCortesFphaNwv))
    with patch("builtins.open", m):
        rel = AvlCortesFpha.read(ARQ_TESTE)
        assert rel.versao == "FPHA_NEWAVE"
        assert rel.tabela.at[0, "codigo_usina"] == 4
        assert rel.tabela.at[0, "periodo"] == 1
        assert rel.tabela.at[0, "nome_usina"] == "FUNIL-GRANDE"
        assert rel.tabela.at[0, "indice_corte"] == 1
        assert rel.tabela.at[0, "fator_correcao"] == 1.0
        assert rel.tabela.at[0, "rhs_energia"] == 0.0
        assert rel.tabela.at[0, "coeficiente_volume_util_MW_hm3"] == 0.0
        assert (
            rel.tabela.at[0, "coeficiente_vazao_turbinada_MW_m3s"]
            == 0.35607775
        )
        assert rel.tabela.at[0, "coeficiente_vazao_vertida_MW_m3s"] == 0.0
        assert rel.tabela.at[0, "coeficiente_vazao_lateral_MW_m3s"] == 0.0


def test_eq_avl_nwv_cortesfpha_nwv():
    m: MagicMock = mock_open(read_data="".join(MockAvlCortesFphaNwv))
    with patch("builtins.open", m):
        rel1 = AvlCortesFpha.read(ARQ_TESTE)
        rel2 = AvlCortesFpha.read(ARQ_TESTE)
        assert rel1 == rel2


def test_neq_avl_nwv_cortesfpha_nwv():
    m: MagicMock = mock_open(read_data="".join(MockAvlCortesFphaNwv))
    with patch("builtins.open", m):
        rel1 = AvlCortesFpha.read(ARQ_TESTE)
        rel2 = AvlCortesFpha.read(ARQ_TESTE)
        rel1.tabela.iloc[0, 0] = -1
        assert rel1 != rel2
