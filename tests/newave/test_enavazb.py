from inewave.newave.modelos.enavazb import SecaoDadosEnavazb
from inewave.newave.enavazb import Enavazb


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch


ARQ_TESTE = "./tests/mocks/arquivos/enavazb.dat"

NUM_FORWARDS = 2
NUM_REES = 1
NUM_ABERTURAS = 20
NUM_ESTAGIOS = 16
NUM_ENTRADAS = NUM_FORWARDS * NUM_ABERTURAS * NUM_REES * NUM_ESTAGIOS


def test_secao_enavaz():
    r = SecaoDadosEnavazb()
    with open(ARQ_TESTE, "rb") as fp:
        r.read(
            fp,
            numero_forwards=NUM_FORWARDS,
            numero_aberturas=NUM_ABERTURAS,
            numero_rees=NUM_REES,
            numero_estagios=NUM_ESTAGIOS,
        )

    assert len(r.data) == NUM_ENTRADAS


def test_atributos_encontrados_enavaz():
    h = Enavazb.read(
        ARQ_TESTE,
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
    )
    assert h.series is not None
    assert h.series.isna().sum().sum() == 0


def test_atributos_nao_encontrados_enavaz():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        h = Enavazb.read(
            ARQ_TESTE,
            numero_forwards=NUM_FORWARDS,
            numero_aberturas=NUM_ABERTURAS,
            numero_rees=NUM_REES,
            numero_estagios=NUM_ESTAGIOS,
        )
        assert h.series.isna().sum().sum() == NUM_ENTRADAS


def test_eq_enavaz():
    h1 = Enavazb.read(
        ARQ_TESTE,
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
    )
    h2 = Enavazb.read(
        ARQ_TESTE,
        numero_forwards=NUM_FORWARDS,
        numero_aberturas=NUM_ABERTURAS,
        numero_rees=NUM_REES,
        numero_estagios=NUM_ESTAGIOS,
    )
    assert h1 == h2
