# Rotinas de testes associadas ao arquivo MEDIAS-UISH.CSV do NWLISTOP
from inewave.nwlistop.mediasusih import Mediasusih

ARQ_TESTE = "tests/_arquivos/MEDIAS-USIH.CSV"


def test_eq_mediasusih():
    leitor = Mediasusih.read(ARQ_TESTE)
    leitor2 = Mediasusih.read(ARQ_TESTE)
    assert leitor == leitor2
    assert leitor.valores.shape == (9840, 30)
