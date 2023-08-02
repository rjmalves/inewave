from inewave.newave.modelos.vazaos import SecaoDadosVazaos
from inewave.newave.vazaos import Vazaos


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch


ARQ_TESTE = "./tests/mocks/arquivos/vazaos.dat"

NUM_SERIES = 2
NUM_UHES = 1
NUM_ESTAGIOS = 16
NUM_ESTAGIOS_TH = 12
NUM_ENTRADAS = NUM_SERIES * NUM_UHES * (NUM_ESTAGIOS_TH + NUM_ESTAGIOS)


def test_secao_vazao():
    r = SecaoDadosVazaos()
    with open(ARQ_TESTE, "rb") as fp:
        r.read(
            fp,
            numero_series=NUM_SERIES,
            numero_uhes=NUM_UHES,
            numero_estagios=NUM_ESTAGIOS,
            numero_estagios_th=NUM_ESTAGIOS_TH,
        )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_vazao():
    h = Vazaos.read(
        ARQ_TESTE,
        numero_series=NUM_SERIES,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_vazao():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        h = Vazaos.read(
            ARQ_TESTE,
            numero_series=NUM_SERIES,
            numero_uhes=NUM_UHES,
            numero_estagios=NUM_ESTAGIOS,
            numero_estagios_th=NUM_ESTAGIOS_TH,
        )
        assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_vazao():
    h1 = Vazaos.read(
        ARQ_TESTE,
        numero_series=NUM_SERIES,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    h2 = Vazaos.read(
        ARQ_TESTE,
        numero_series=NUM_SERIES,
        numero_uhes=NUM_UHES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h1 == h2
