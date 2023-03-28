from inewave.newave.modelos.vazaoaf import SecaoDadosVazaoaf
from inewave.newave.vazaoaf import Vazaoaf

from os.path import join
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch


ARQ_TEST = "./tests/mocks/arquivos"

NUM_FORWARDS = 2
NUM_UHES = 1
NUM_ESTAGIOS = 16
NUM_ESTAGIOS_TH = 12
NUM_ENTRADAS = NUM_FORWARDS * NUM_UHES * (NUM_ESTAGIOS_TH + NUM_ESTAGIOS)


def test_secao_vazao():
    r = SecaoDadosVazaoaf()
    with open(join(ARQ_TEST, "vazaoaf.dat"), "rb") as fp:
        r.read(
            fp,
            numero_forwards=NUM_FORWARDS,
            numero_uhes=NUM_UHES,
            numero_estagios=NUM_ESTAGIOS,
            numero_estagios_th=NUM_ESTAGIOS_TH,
        )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_vazao():
    h = Vazaoaf.le_arquivo(
        ARQ_TEST,
        numero_forwards=NUM_FORWARDS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_vazao():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        h = Vazaoaf.le_arquivo(
            "",
            numero_forwards=NUM_FORWARDS,
            numero_uhes=NUM_UHES,
            numero_estagios=NUM_ESTAGIOS,
            numero_estagios_th=NUM_ESTAGIOS_TH,
        )
        assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_vazao():
    h1 = Vazaoaf.le_arquivo(
        ARQ_TEST,
        numero_forwards=NUM_FORWARDS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    h2 = Vazaoaf.le_arquivo(
        ARQ_TEST,
        numero_forwards=NUM_FORWARDS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h1 == h2
