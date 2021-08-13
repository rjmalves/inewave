# Rotinas de testes associadas ao arquivo MEDIAS-SIN.CSV do NWLISTOP
from inewave.nwlistop.mediassin import MediasSIN
import pandas as pd  # type: ignore


leitor = MediasSIN.le_arquivo("tests/_arquivos")


def test_eq_mediasmerc():
    leitor2 = MediasSIN.le_arquivo("tests/_arquivos")
    assert leitor == leitor2


def test_neq_mediassin():
    leitor2 = MediasSIN.le_arquivo("tests/_arquivos")
    leitor2.medias = pd.DataFrame()
    assert leitor != leitor2
