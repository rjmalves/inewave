# Rotinas de testes associadas ao arquivo MEDIAS-RHV.CSV do NWLISTOP
from inewave.nwlistop.mediasrhv import Mediasrhv

ARQ_TESTE = "tests/_arquivos/MEDIAS-RHV.CSV"


def test_eq_mediasrhv():
    leitor = Mediasrhv.read(ARQ_TESTE)
    leitor2 = Mediasrhv.read(ARQ_TESTE)
    assert leitor == leitor2
    assert leitor.valores.shape == (0, 2)
