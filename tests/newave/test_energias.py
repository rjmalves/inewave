from inewave.newave.modelos.energias import SecaoDadosEnergias
from inewave.newave.energias import Energias

from os.path import join
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch


ARQ_TEST = "./tests/mocks/arquivos"

NUM_SERIES = 2
NUM_REES = 1
NUM_ESTAGIOS = 16
NUM_ESTAGIOS_TH = 12
NUM_ENTRADAS = NUM_SERIES * NUM_REES * (NUM_ESTAGIOS_TH + NUM_ESTAGIOS)


def test_secao_energia():
    r = SecaoDadosEnergias()
    with open(join(ARQ_TEST, "energias.dat"), "rb") as fp:
        r.read(
            fp,
            numero_series=NUM_SERIES,
            numero_rees=NUM_REES,
            numero_estagios=NUM_ESTAGIOS,
            numero_estagios_th=NUM_ESTAGIOS_TH,
        )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_energia():
    h = Energias.le_arquivo(
        ARQ_TEST,
        numero_series=NUM_SERIES,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_energia():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        h = Energias.le_arquivo(
            "",
            numero_series=NUM_SERIES,
            numero_rees=NUM_REES,
            numero_estagios=NUM_ESTAGIOS,
            numero_estagios_th=NUM_ESTAGIOS_TH,
        )
        assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_energia():
    h1 = Energias.le_arquivo(
        ARQ_TEST,
        numero_series=NUM_SERIES,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    h2 = Energias.le_arquivo(
        ARQ_TEST,
        numero_series=NUM_SERIES,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h1 == h2
