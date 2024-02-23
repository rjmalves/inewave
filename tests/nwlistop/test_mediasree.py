# Rotinas de testes associadas ao arquivo MEDIAS-REE.CSV do NWLISTOP
from inewave.nwlistop.mediasree import Mediasree


ARQ_TESTE = "tests/_arquivos/MEDIAS-REE.CSV"


def test_eq_mediasree():
    leitor = Mediasree.read(ARQ_TESTE)
    leitor2 = Mediasree.read(ARQ_TESTE)
    assert leitor == leitor2
    assert leitor.valores.shape == (720, 49)
