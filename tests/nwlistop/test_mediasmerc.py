# Rotinas de testes associadas ao arquivo MEDIAS-MERC.CSV do NWLISTOP
from inewave.nwlistop.mediasmerc import MediasMerc
import pandas as pd  # type: ignore


leitor = MediasMerc.le_arquivo("tests/_arquivos")


def test_eq_mediasmerc():
    leitor2 = MediasMerc.le_arquivo("tests/_arquivos")
    assert leitor == leitor2


def test_neq_mediasmerc():
    leitor2 = MediasMerc.le_arquivo("tests/_arquivos")
    leitor2.medias = pd.DataFrame()
    assert leitor != leitor2
