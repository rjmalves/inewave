# Rotinas de testes associadas ao arquivo MEDIAS-RHQ.CSV do NWLISTOP
from inewave.nwlistop.mediasrhq import Mediasrhq


ARQ_TESTE = "tests/_arquivos/MEDIAS-RHQ.CSV"


def test_eq_mediasrhq():
    leitor = Mediasrhq.read(ARQ_TESTE)
    leitor2 = Mediasrhq.read(ARQ_TESTE)
    assert leitor == leitor2
    assert leitor.valores.shape == (0, 2)
