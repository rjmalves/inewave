from inewave.nwlistcf.estados import LeituraEstados

leitor = LeituraEstados("./tests/_arquivos")
leitor.le_arquivo()


def test_leitura():
    assert len(leitor.estados.registros.keys()) > 0


def test_eq_estados():
    leitor2 = LeituraEstados("./tests/_arquivos")
    leitor2.le_arquivo()
    assert leitor2.estados == leitor.estados


def test_neq_estados():
    leitor2 = LeituraEstados("./tests/_arquivos")
    leitor2.le_arquivo()
    leitor2.estados.registros[5] = {}
    assert leitor2.estados != leitor.estados
