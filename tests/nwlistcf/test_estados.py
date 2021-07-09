from inewave.nwlistcf.estados import Estados

est = Estados.le_arquivo("./tests/_arquivos")


def test_leitura():
    assert len(est.registros) > 0


def test_eq_estados():
    est2 = Estados.le_arquivo("./tests/_arquivos")
    assert est == est2


# def test_neq_estados():
#     leitor2 = LeituraEstados("./tests/_arquivos")
#     leitor2.le_arquivo()
#     leitor2.estados.registros[5] = {}
#     assert leitor2.estados != leitor.estados
