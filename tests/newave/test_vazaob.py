from inewave.newave.modelos.vazaob import SecaoDadosVazaob
from inewave.newave.vazaob import Vazaob

from tests.mocks.binarios import bytes_gz, fp_gz


ARQ_TESTE = "./tests/mocks/arquivos/vazaob.dat"

NUM_FORWARDS = 2
NUM_ABERTURAS = 20
NUM_UHES = 1
NUM_ESTAGIOS = 16
NUM_ENTRADAS = NUM_FORWARDS * NUM_ABERTURAS * NUM_UHES * NUM_ESTAGIOS


def test_secao_vazao():
    r = SecaoDadosVazaob()
    r.read(
        fp_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
    )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_vazao():
    h = Vazaob.read(
        bytes_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_vazao():
    h = Vazaob.read(
        b"",
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
    )
    assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_vazao():
    h1 = Vazaob.read(
        bytes_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
    )
    h2 = Vazaob.read(
        bytes_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
    )
    assert h1 == h2


# NOTE: Binary file with parametrized read, round-trip requires external dimensions
