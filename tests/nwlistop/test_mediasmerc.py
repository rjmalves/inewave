# Rotinas de testes associadas ao arquivo MEDIAS-MERC.CSV do NWLISTOP
from inewave.nwlistop.mediasmerc import Mediasmerc
import pandas as pd  # type: ignore


leitor = Mediasmerc.le_arquivo("tests/_arquivos")


def test_eq_mediasmerc():
    leitor2 = Mediasmerc.le_arquivo("tests/_arquivos")
    assert leitor == leitor2


def test_neq_mediasmerc():
    leitor2 = Mediasmerc.le_arquivo("tests/_arquivos")
    leitor2.medias = pd.DataFrame()
    assert leitor != leitor2
