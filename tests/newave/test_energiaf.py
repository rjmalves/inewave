from inewave.newave.modelos.energiaf import SecaoDadosEnergiaf
from inewave.newave.energiaf import Energiaf

from os.path import join
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch


ARQ_TEST = "./tests/mocks/arquivos"

NUM_FORWARDS = 2
NUM_REES = 1
NUM_ESTAGIOS = 16
NUM_ESTAGIOS_TH = 12
NUM_ENTRADAS = NUM_FORWARDS * NUM_REES * (NUM_ESTAGIOS_TH + NUM_ESTAGIOS)


def test_secao_energia():
    r = SecaoDadosEnergiaf()
    with open(join(ARQ_TEST, "energiaf.dat"), "rb") as fp:
        r.read(
            fp,
            numero_forwards=NUM_FORWARDS,
            numero_rees=NUM_REES,
            numero_estagios=NUM_ESTAGIOS,
            numero_estagios_th=NUM_ESTAGIOS_TH,
        )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_energia():
    h = Energiaf.le_arquivo(
        ARQ_TEST,
        numero_forwards=NUM_FORWARDS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_energia():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        h = Energiaf.le_arquivo(
            "",
            numero_forwards=NUM_FORWARDS,
            numero_rees=NUM_REES,
            numero_estagios=NUM_ESTAGIOS,
            numero_estagios_th=NUM_ESTAGIOS_TH,
        )
        assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_energia():
    h1 = Energiaf.le_arquivo(
        ARQ_TEST,
        numero_forwards=NUM_FORWARDS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    h2 = Energiaf.le_arquivo(
        ARQ_TEST,
        numero_forwards=NUM_FORWARDS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h1 == h2
