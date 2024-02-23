# Rotinas de testes associadas ao arquivo MEDIAS-SIN.CSV do NWLISTOP
from inewave.nwlistop.mediassin import Mediassin


ARQ_TESTE = "tests/_arquivos/MEDIAS-SIN.CSV"


def test_eq_mediassin():
    leitor = Mediassin.read(ARQ_TESTE)
    leitor2 = Mediassin.read(ARQ_TESTE)
    assert leitor == leitor2
    assert leitor.valores.shape == (57, 55)
