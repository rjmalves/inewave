# Rotinas de testes associadas ao arquivo MEDIAS-REP.CSV do NWLISTOP
from inewave.nwlistop.mediasrep import Mediasrep


ARQ_TESTE = "tests/_arquivos/MEDIAS-REP.CSV"


def test_eq_mediasrep():
    leitor = Mediasrep.read(ARQ_TESTE)
    leitor2 = Mediasrep.read(ARQ_TESTE)
    assert leitor == leitor2
    assert leitor.valores.shape == (0, 2)
