# Rotinas de testes associadas ao arquivo MEDIAS-SIN.CSV do NWLISTOP
from inewave.nwlistop.mediassin import MediasSIN
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


leitor = MediasSIN.le_arquivo("tests/_arquivos")


def test_eq_mediasmerc():
    leitor2 = MediasSIN.le_arquivo("tests/_arquivos")
    assert leitor == leitor2


def test_neq_mediassin():
    leitor2 = MediasSIN.le_arquivo("tests/_arquivos")
    leitor2.dados = pd.DataFrame()
    assert leitor != leitor2


def test_alinhamento_horizontal():
    # Confere se todos os valores de geracao eolica e solar
    # são nulos
    eol = leitor.geracao_eolica
    sol = leitor.geracao_solar
    for e, s in zip(eol, sol):
        assert np.all(e == 0.0)
        assert np.all(s == 0.0)


def test_valores_vertimento():
    # Confere se todos os valores de vertimentos controláveis
    # e fio d'água somam o total, a menos da precisão.
    vert_total = leitor.vertimento_total
    vert_control = leitor.vertimento_controlavel
    vert_fio = leitor.vertimento_fio_dagua
    for t, c, f in zip(vert_total,
                       vert_control,
                       vert_fio):
        assert np.all(t - c - f < 1e-1)


def test_energias_armazenadas():
    e = leitor.energias_armazenadas_absolutas
    assert len(e) > 0
    e = leitor.energias_armazenadas_percentuais
    assert len(e) > 0


def test_percentis_energias():
    e = leitor.percentil_10_energias_armazenadas
    assert len(e) > 0
    e = leitor.percentil_20_energias_armazenadas
    assert len(e) > 0
    e = leitor.percentil_30_energias_armazenadas
    assert len(e) > 0
    e = leitor.percentil_40_energias_armazenadas
    assert len(e) > 0
    e = leitor.percentil_50_energias_armazenadas
    assert len(e) > 0
    e = leitor.percentil_60_energias_armazenadas
    assert len(e) > 0
    e = leitor.percentil_70_energias_armazenadas
    assert len(e) > 0
    e = leitor.percentil_80_energias_armazenadas
    assert len(e) > 0
    e = leitor.percentil_90_energias_armazenadas
    assert len(e) > 0
    e = leitor.percentil_100_energias_armazenadas
    assert len(e) > 0


def test_energias_afluentes():
    e = leitor.energia_natural_afluente
    assert len(e) > 0
    e = leitor.energia_controlavel_corrigida
    assert len(e) > 0
    e = leitor.energia_fio_dagua_bruta
    assert len(e) > 0
    e = leitor.energia_fio_dagua_liquida
    assert len(e) > 0
    e = leitor.energia_evaporada
    assert len(e) > 0


def test_geracoes():
    e = leitor.geracao_hidraulica_controlavel
    assert len(e) > 0
    e = leitor.geracao_hidraulica_fio_dagua_liquida
    assert len(e) > 0
    e = leitor.geracao_hidraulica_total
    assert len(e) > 0
    e = leitor.geracao_eolica
    assert len(e) > 0
    e = leitor.geracao_solar
    assert len(e) > 0
    e = leitor.geracao_termica
    assert len(e) > 0


def test_custos():
    e = leitor.deficit
    assert len(e) > 0
    e = leitor.custo_deficit
    assert len(e) > 0
    e = leitor.custo_termica
    assert len(e) > 0
