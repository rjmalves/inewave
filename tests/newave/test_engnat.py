from inewave.newave.modelos.engnat import SecaoDadosEngnat
from inewave.newave.engnat import Engnat
from inewave.config import MAX_ANOS_HISTORICO
from os.path import join
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch


ARQ_TEST = "./tests/mocks/arquivos"

NUM_CONFIGURACOES = 1
NUM_REES = 12
ANO_INICIO_HISTORICO = 1931
NUM_ENTRADAS = NUM_CONFIGURACOES * NUM_REES * 12 * MAX_ANOS_HISTORICO


def test_secao_engnat():
    r = SecaoDadosEngnat()
    with open(join(ARQ_TEST, "engnat.dat"), "rb") as fp:
        r.read(
            fp,
            numero_rees=NUM_REES,
            ano_inicio_historico=ANO_INICIO_HISTORICO,
            numero_configuracoes=NUM_CONFIGURACOES,
        )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_engnat():
    h = Engnat.le_arquivo(
        ARQ_TEST,
        numero_rees=NUM_REES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_engnat():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        h = Engnat.le_arquivo(
            "",
            numero_rees=NUM_REES,
            ano_inicio_historico=ANO_INICIO_HISTORICO,
            numero_configuracoes=NUM_CONFIGURACOES,
        )
        assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_engnat():
    h1 = Engnat.le_arquivo(
        ARQ_TEST,
        numero_rees=NUM_REES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )
    h2 = Engnat.le_arquivo(
        ARQ_TEST,
        numero_rees=NUM_REES,
        ano_inicio_historico=ANO_INICIO_HISTORICO,
        numero_configuracoes=NUM_CONFIGURACOES,
    )
    assert h1 == h2
