from inewave.newave.modelos.enavazb import SecaoDadosEnavazb
from inewave.newave.enavazb import Enavazb

from tests.mocks.binarios import bytes_gz, fp_gz


ARQ_TESTE = "./tests/mocks/arquivos/enavazb.dat"

NUM_FORWARDS = 2
NUM_REES = 1
NUM_ABERTURAS = 20
NUM_ESTAGIOS = 16
NUM_ENTRADAS = NUM_FORWARDS * NUM_ABERTURAS * NUM_REES * NUM_ESTAGIOS


def test_secao_enavaz():
    r = SecaoDadosEnavazb()
    r.read(
        fp_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
    )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_enavaz():
    h = Enavazb.read(
        bytes_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_enavaz():
    h = Enavazb.read(
        b"",
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
    )
    assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_enavaz():
    h1 = Enavazb.read(
        bytes_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
    )
    h2 = Enavazb.read(
        bytes_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
    )
    assert h1 == h2


# NOTE: Binary file with parametrized read, round-trip requires external dimensions
