from inewave.newave.modelos.energiab import SecaoDadosEnergiab
from inewave.newave.energiab import Energiab

from tests.mocks.binarios import bytes_gz, fp_gz


ARQ_TESTE = "./tests/mocks/arquivos/energiab.dat"

NUM_FORWARDS = 2
NUM_REES = 1
NUM_ABERTURAS = 20
NUM_ESTAGIOS = 16
NUM_ENTRADAS = NUM_FORWARDS * NUM_ABERTURAS * NUM_REES * NUM_ESTAGIOS


def test_secao_energia():
    r = SecaoDadosEnergiab()
    r.read(
        fp_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
    )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_energia():
    h = Energiab.read(
        bytes_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_energia():
    h = Energiab.read(
        b"",
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
    )
    assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_energia():
    h1 = Energiab.read(
        bytes_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
    )
    h2 = Energiab.read(
        bytes_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
    )
    assert h1 == h2


# NOTE: Binary file with parametrized read, round-trip requires external dimensions
