# Rotinas de testes associadas ao arquivo MEDIAS-SIN.CSV do NWLISTOP
from inewave.nwlistop.mediassin import Mediassin
import pandas as pd  # type: ignore


leitor = Mediassin.le_arquivo("tests/_arquivos")


def test_eq_mediassin():
    leitor2 = Mediassin.le_arquivo("tests/_arquivos")
    assert leitor == leitor2


def test_neq_mediassin():
    leitor2 = Mediassin.le_arquivo("tests/_arquivos")
    leitor2.medias = pd.DataFrame()
    assert leitor != leitor2
