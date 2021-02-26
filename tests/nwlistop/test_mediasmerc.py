# Rotinas de testes associadas ao arquivo MEDIAS-MERC.CSV do NWLISTOP
from inewave.nwlistop.mediasmerc import LeituraMediasMerc
import numpy as np  # type: ignore


leitor = LeituraMediasMerc("tests/_arquivos")
leitor.le_arquivo()


def test_leitura():
    assert leitor.medias.mes_pmo != 0


def test_eq_mediasmerc():
    leitor2 = LeituraMediasMerc("tests/_arquivos")
    leitor2.le_arquivo()
    assert leitor.medias == leitor2.medias


def test_neq_mediasmerc():
    leitor2 = LeituraMediasMerc("tests/_arquivos")
    leitor2.le_arquivo()
    leitor2.medias.tabela = np.array([])
    assert leitor.medias != leitor2.medias


def test_alinhamento_vertical():
    mes_pmo = leitor.medias.mes_pmo
    # Confere se todos os valores anteriores ao mês
    # do PMO são nulos
    assert np.all(leitor.medias.tabela[:, :mes_pmo-1] == 0)


def test_alinhamento_horizontal():
    # Confere se todos os valores de geracao eolica e solar
    # são nulos
    eol = leitor.medias.geracao_eolica
    sol = leitor.medias.geracao_solar
    for e, s in zip(eol.values(), sol.values()):
        assert np.all(e == 0.0)
        assert np.all(s == 0.0)


def test_valores_vertimento():
    # Confere se todos os valores de vertimentos controláveis
    # e fio d'água somam o total, a menos da precisão.
    vert_total = leitor.medias.vertimento_total
    vert_control = leitor.medias.vertimento_controlavel
    vert_fio = leitor.medias.vertimento_fio_dagua
    for t, c, f in zip(vert_total.values(),
                       vert_control.values(),
                       vert_fio.values()):
        assert np.all(t - c - f < 1e-1)


def test_energias_armazenadas():
    e = leitor.medias.energias_armazenadas_absolutas
    assert len(e.keys()) > 0
    e = leitor.medias.energias_armazenadas_percentuais
    assert len(e.keys()) > 0


def test_percentis_energias():
    e = leitor.medias.percentil_10_energias_armazenadas
    assert len(e.keys()) > 0
    e = leitor.medias.percentil_20_energias_armazenadas
    assert len(e.keys()) > 0
    e = leitor.medias.percentil_30_energias_armazenadas
    assert len(e.keys()) > 0
    e = leitor.medias.percentil_40_energias_armazenadas
    assert len(e.keys()) > 0
    e = leitor.medias.percentil_50_energias_armazenadas
    assert len(e.keys()) > 0
    e = leitor.medias.percentil_60_energias_armazenadas
    assert len(e.keys()) > 0
    e = leitor.medias.percentil_70_energias_armazenadas
    assert len(e.keys()) > 0
    e = leitor.medias.percentil_80_energias_armazenadas
    assert len(e.keys()) > 0
    e = leitor.medias.percentil_90_energias_armazenadas
    assert len(e.keys()) > 0
    e = leitor.medias.percentil_100_energias_armazenadas
    assert len(e.keys()) > 0


def test_energias_afluentes():
    e = leitor.medias.energia_natural_afluente
    assert len(e.keys()) > 0
    e = leitor.medias.energia_controlavel_corrigida
    assert len(e.keys()) > 0
    e = leitor.medias.energia_fio_dagua_bruta
    assert len(e.keys()) > 0
    e = leitor.medias.energia_fio_dagua_liquida
    assert len(e.keys()) > 0
    e = leitor.medias.energia_evaporada
    assert len(e.keys()) > 0


def test_geracoes():
    e = leitor.medias.geracao_hidraulica_controlavel
    assert len(e.keys()) > 0
    e = leitor.medias.geracao_hidraulica_fio_dagua_liquida
    assert len(e.keys()) > 0
    e = leitor.medias.geracao_hidraulica_total
    assert len(e.keys()) > 0
    e = leitor.medias.geracao_eolica
    assert len(e.keys()) > 0
    e = leitor.medias.geracao_solar
    assert len(e.keys()) > 0
    e = leitor.medias.geracao_termica
    assert len(e.keys()) > 0


def test_custos():
    e = leitor.medias.deficit
    assert len(e.keys()) > 0
    e = leitor.medias.custo_marginal_operacao
    assert len(e.keys()) > 0
    e = leitor.medias.custo_deficit
    assert len(e.keys()) > 0
    e = leitor.medias.custo_termica
    assert len(e.keys()) > 0
