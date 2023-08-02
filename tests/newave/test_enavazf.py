from inewave.newave.modelos.enavazf import SecaoDadosEnavazf
from inewave.newave.enavazf import Enavazf


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch


ARQ_TESTE = "./tests/mocks/arquivos/enavazf.dat"

NUM_FORWARDS = 2
NUM_REES = 1
NUM_ESTAGIOS = 16
NUM_ESTAGIOS_TH = 12
NUM_ENTRADAS = NUM_FORWARDS * NUM_REES * (NUM_ESTAGIOS_TH + NUM_ESTAGIOS)


def test_secao_enavaz():
    r = SecaoDadosEnavazf()
    with open(ARQ_TESTE, "rb") as fp:
        r.read(
            fp,
            numero_forwards=NUM_FORWARDS,
            numero_rees=NUM_REES,
            numero_estagios=NUM_ESTAGIOS,
            numero_estagios_th=NUM_ESTAGIOS_TH,
        )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_enavaz():
    h = Enavazf.read(
        ARQ_TESTE,
        numero_forwards=NUM_FORWARDS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_enavaz():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        h = Enavazf.read(
            ARQ_TESTE,
            numero_forwards=NUM_FORWARDS,
            numero_rees=NUM_REES,
            numero_estagios=NUM_ESTAGIOS,
            numero_estagios_th=NUM_ESTAGIOS_TH,
        )
        assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_enavaz():
    h1 = Enavazf.read(
        ARQ_TESTE,
        numero_forwards=NUM_FORWARDS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    h2 = Enavazf.read(
        ARQ_TESTE,
        numero_forwards=NUM_FORWARDS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
        numero_estagios_th=NUM_ESTAGIOS_TH,
    )
    assert h1 == h2
