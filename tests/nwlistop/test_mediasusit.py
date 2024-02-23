# Rotinas de testes associadas ao arquivo MEDIAS-USIT.CSV do NWLISTOP
from inewave.nwlistop.mediasusit import Mediasusit


ARQ_TESTE = "tests/_arquivos/MEDIAS-USIT.CSV"


def test_eq_mediasusit():
    leitor = Mediasusit.read(ARQ_TESTE)
    leitor2 = Mediasusit.read(ARQ_TESTE)
    assert leitor == leitor2
    assert leitor.valores.shape == (7680, 5)
