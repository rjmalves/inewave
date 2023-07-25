from inewave.newave.avl_desvfpha_v_q import AvlDesvFphaVQ
import pandas as pd  # type: ignore
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.avl_desvfpha_v_q import MockAvlDesvFphaVQ

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_avl_desvfpha_v_q():
    m: MagicMock = mock_open(read_data="".join(MockAvlDesvFphaVQ))
    with patch("builtins.open", m):
        rel = AvlDesvFphaVQ.read(ARQ_TESTE)
        assert rel.versao == "FPHA_NEWAVE"
        assert rel.tabela.at[0, "codigo_usina"] == 4
        assert rel.tabela.at[0, "nome_usina"] == "FUNIL-GRANDE"
        assert pd.isna(rel.tabela.at[0, "volume_armazenado_percentual"])
        assert rel.tabela.at[0, "vazao_turbinada_m3s"] == 0.0
        assert rel.tabela.at[0, "desvio_percentual"] == 0.0


def test_eq_avl_desvfpha_v_q():
    m: MagicMock = mock_open(read_data="".join(MockAvlDesvFphaVQ))
    with patch("builtins.open", m):
        rel1 = AvlDesvFphaVQ.read(ARQ_TESTE)
        rel2 = AvlDesvFphaVQ.read(ARQ_TESTE)
        assert rel1 == rel2


## Não precisa comparar isto, é somente leitura - passa por agregação
# def test_neq_avl_desvfpha_v_q():
#     m: MagicMock = mock_open(read_data="".join(MockAvlDesvFphaVQ))
#     with patch("builtins.open", m):
#         rel1 = AvlDesvFphaVQ.read(ARQ_TESTE)
#         rel2 = AvlDesvFphaVQ.read(ARQ_TESTE)
#         rel1.tabela.iloc[0, 0] = -1
#         assert rel1 != rel2
