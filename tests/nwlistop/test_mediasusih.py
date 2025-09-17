# Rotinas de testes associadas ao arquivo MEDIAS-UISH.CSV do NWLISTOP
from inewave.nwlistop.mediasusih import Mediasusih

TESTES = [{"file": "tests/_arquivos/MEDIAS-USIH.CSV", "rows": 9840},
          {"file": "tests/_arquivos/MEDIAS-USIH-2.CSV", "rows": 8281}]

def test_eq_mediasusih():
    for teste in TESTES:
        leitor = Mediasusih.read(teste["file"])
        leitor2 = Mediasusih.read(teste["file"])
        assert leitor == leitor2
        assert leitor.valores.shape == (teste["rows"], 30)
