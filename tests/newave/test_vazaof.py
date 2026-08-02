from inewave.newave.modelos.vazaof import SecaoDadosVazaof
from inewave.newave.vazaof import Vazaof

from tests.mocks.binarios import bytes_gz, fp_gz


ARQ_TESTE = "./tests/mocks/arquivos/vazaof.dat"

NUM_FORWARDS = 2
NUM_UHES = 1
NUM_ESTAGIOS = 16
NUM_ESTAGIOS_TH = 12
NUM_ENTRADAS = NUM_FORWARDS * NUM_UHES * (NUM_ESTAGIOS_TH + NUM_ESTAGIOS)


def test_secao_vazao():
    r = SecaoDadosVazaof()
    r.read(
        fp_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_vazao():
    h = Vazaof.read(
        bytes_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_vazao():
    h = Vazaof.read(
        b"",
        numero_forwards=NUM_FORWARDS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_vazao():
    h1 = Vazaof.read(
        bytes_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    h2 = Vazaof.read(
        bytes_gz(ARQ_TESTE),
        numero_forwards=NUM_FORWARDS,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h1 == h2


# NOTE: Binary file with parametrized read, round-trip requires external dimensions
