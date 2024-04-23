from inewave.newave.fpha_avl_desv_s import FphaAvlDesvS

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.avl_desvfpha_s import MockAvlDesvFphaS

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_fpha_avl_desv_s():
    m: MagicMock = mock_open(read_data="".join(MockAvlDesvFphaS))
    with patch("builtins.open", m):
        rel = FphaAvlDesvS.read(ARQ_TESTE)
        assert rel.versao == "FPHA_NEWAVE"
        assert rel.tabela.at[0, "codigo_usina"] == 4
        assert rel.tabela.at[0, "nome_usina"] == "FUNIL-GRANDE"
        assert rel.tabela.at[0, "volume_armazenado_percentual"] == 100.0
        assert rel.tabela.at[0, "vazao_turbinada_m3s"] == 0.0
        assert rel.tabela.at[0, "vazao_vertida_m3s"] == 0.0
        assert rel.tabela.at[0, "desvio_percentual"] == 0.0


def test_es_fpha_avl_desv_s():
    m: MagicMock = mock_open(read_data="".join(MockAvlDesvFphaS))
    with patch("builtins.open", m):
        rel1 = FphaAvlDesvS.read(ARQ_TESTE)
        rel2 = FphaAvlDesvS.read(ARQ_TESTE)
        assert rel1 == rel2


## Não precisa comparar isto, é somente leitura - passa por agregação
# def test_nes_fpha_avl_desv_s():
#     m: MagicMock = mock_open(read_data="".join(MockAvlDesvFphaS))
#     with patch("builtins.open", m):
#         rel1 = AvlDesvFphaS.read(ARQ_TESTE)
#         rel2 = AvlDesvFphaS.read(ARQ_TESTE)
#         rel1.tabela.iloc[0, 0] = -1
#         assert rel1 != rel2
