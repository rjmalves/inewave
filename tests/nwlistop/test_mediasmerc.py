# Rotinas de testes associadas ao arquivo MEDIAS-MERC.CSV do NWLISTOP
from inewave.nwlistop.mediasmerc import Mediasmerc


ARQ_TESTE = "tests/_arquivos/MEDIAS-MERC.CSV"


def test_eq_mediasmerc():
    leitor = Mediasmerc.read(ARQ_TESTE)
    leitor2 = Mediasmerc.read(ARQ_TESTE)
    assert leitor == leitor2
    assert leitor.valores.shape == (228, 54)


# NOTE: MEDIAS CSV file, SectionFile with pd.read_csv, no write path
