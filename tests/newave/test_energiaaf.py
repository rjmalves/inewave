from inewave.newave.modelos.energiaaf import SecaoDadosEnergiaaf
from inewave.newave.energiaaf import Energiaaf

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
    r = SecaoDadosEnergiaaf()
    with open(join(ARQ_TEST, "energiaaf.dat"), "rb") as fp:
        r.read(
            fp,
            numero_forwards=NUM_FORWARDS,
            numero_rees=NUM_REES,
            numero_estagios=NUM_ESTAGIOS,
            numero_estagios_th=NUM_ESTAGIOS_TH,
        )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_energia():
    h = Energiaaf.le_arquivo(
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
        h = Energiaaf.le_arquivo(
            "",
            numero_forwards=NUM_FORWARDS,
            numero_rees=NUM_REES,
            numero_estagios=NUM_ESTAGIOS,
            numero_estagios_th=NUM_ESTAGIOS_TH,
        )
        assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_energia():
    h1 = Energiaaf.le_arquivo(
        ARQ_TEST,
        numero_forwards=NUM_FORWARDS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    h2 = Energiaaf.le_arquivo(
        ARQ_TEST,
        numero_forwards=NUM_FORWARDS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h1 == h2
