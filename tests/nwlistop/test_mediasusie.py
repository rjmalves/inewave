# Rotinas de testes associadas ao arquivo MEDIAS-USIE.CSV do NWLISTOP
from inewave.nwlistop.mediasusie import Mediasusie


ARQ_TESTE = "tests/_arquivos/MEDIAS-USIE.CSV"


def test_eq_mediasusie():
    leitor = Mediasusie.read(ARQ_TESTE)
    leitor2 = Mediasusie.read(ARQ_TESTE)
    assert leitor == leitor2
    assert leitor.valores.shape == (0, 2)
