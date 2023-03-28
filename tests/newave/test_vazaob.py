from inewave.newave.modelos.vazaob import SecaoDadosVazaob
from inewave.newave.vazaob import Vazaob

from os.path import join
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch


ARQ_TEST = "./tests/mocks/arquivos"

NUM_FORWARDS = 2
NUM_ABERTURAS = 20
NUM_UHES = 1
NUM_ESTAGIOS = 16
NUM_ENTRADAS = NUM_FORWARDS * NUM_ABERTURAS * NUM_UHES * NUM_ESTAGIOS


def test_secao_vazao():
    r = SecaoDadosVazaob()
    with open(join(ARQ_TEST, "vazaob.dat"), "rb") as fp:
        r.read(
            fp,
            numero_forwards=NUM_FORWARDS,
            numero_aberturas=NUM_ABERTURAS,
            numero_uhes=NUM_UHES,
            numero_estagios=NUM_ESTAGIOS,
        )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_vazao():
    h = Vazaob.le_arquivo(
        ARQ_TEST,
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_vazao():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        h = Vazaob.le_arquivo(
            "",
            numero_forwards=NUM_FORWARDS,
            numero_aberturas=NUM_ABERTURAS,
            numero_uhes=NUM_UHES,
            numero_estagios=NUM_ESTAGIOS,
        )
        assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_vazao():
    h1 = Vazaob.le_arquivo(
        ARQ_TEST,
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
    )
    h2 = Vazaob.le_arquivo(
        ARQ_TEST,
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
    )
    assert h1 == h2
