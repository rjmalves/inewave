# Rotinas de testes associadas ao arquivo MEDIAS-MERC.CSV do NWLISTOP
from inewave.nwlistop.mediasmerc import Mediasmerc
import pandas as pd  # type: ignore


ARQ_TESTE = "tests/_arquivos/MEDIAS-MERC.CSV"


def test_eq_mediasmerc():
    leitor = Mediasmerc.read(ARQ_TESTE)
    leitor2 = Mediasmerc.read(ARQ_TESTE)
    assert leitor == leitor2
    assert leitor.valores.shape == (228, 54)
