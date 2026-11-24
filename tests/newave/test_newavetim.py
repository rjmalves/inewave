from datetime import datetime, timedelta
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from inewave.newave.modelos.newavetim import (
    BlocoTemposEtapasTim,
    BlocoTemposIteracoesTim,
    BlocoVersaoModeloTim,
)
from inewave.newave.newavetim import Newavetim
from tests.mocks.arquivos.newavetim import (
    MockBlocoTemposEtapas,
    MockBlocoTemposIteracoes,
    MockBlocoTemposIteracoesIncompleto,
    MockBlocoVersaoModelo,
    MockNewaveTim,
    MockNewaveTim315,
    MockNewaveTim3004,
    MockNewaveTim3102,
)
from tests.mocks.mock_open import mock_open

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_tempos_etapas():
    m: MagicMock = mock_open(read_data="".join(MockBlocoTemposEtapas))
    b = BlocoTemposEtapasTim()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.shape[0] == 5
    assert b.data.shape[1] == 2
    assert b.data.iloc[0, 0] == "Leitura de Dados"
    assert b.data.iloc[-1, -1] == timedelta(hours=3, minutes=26, seconds=7)


def test_tempos_iteracoes():
    m: MagicMock = mock_open(read_data="".join(MockBlocoTemposIteracoes))
    b = BlocoTemposIteracoesTim()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.columns.tolist() == [
        "iteracao",
        "backward",
        "forward",
        "total",
    ]
    assert b.data["iteracao"].tolist() == [1, 2]
    # Os tempos sem sentido da primeira iteração são mantidos como escritos
    assert b.data.loc[0, "backward"] == timedelta(
        hours=110, minutes=46, seconds=23
    )
    assert b.data.loc[0, "forward"] == timedelta(
        hours=633, minutes=13, seconds=39
    )
    assert b.data.loc[0, "total"] == timedelta(seconds=2)
    assert b.data.loc[1, "backward"] == timedelta(seconds=1.5)
    assert b.data.loc[1, "total"] == timedelta(seconds=4.5)


def test_tempos_iteracoes_ignora_iteracao_incompleta():
    m: MagicMock = mock_open(
        read_data="".join(MockBlocoTemposIteracoesIncompleto)
    )
    b = BlocoTemposIteracoesTim()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data["iteracao"].tolist() == [1]


def test_versao_modelo():
    m: MagicMock = mock_open(read_data="".join(MockBlocoVersaoModelo))
    b = BlocoVersaoModeloTim()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == "28.6.3_CPAMP"


def test_atributos_encontrados_newavetim():
    m: MagicMock = mock_open(read_data="".join(MockNewaveTim))
    with patch("builtins.open", m):
        nt = Newavetim.read(ARQ_TESTE)
        assert nt.tempos_etapas is not None
        assert nt.versao_modelo is not None
        tempos = nt.tempos_iteracoes
        assert tempos is not None
        assert tempos["iteracao"].tolist() == list(range(1, 51))
        assert tempos.loc[49, "total"] == timedelta(minutes=6, seconds=25)


def test_atributos_nao_encontrados_newavetim():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        nt = Newavetim.read(ARQ_TESTE)
        assert nt.tempos_etapas is None
        assert nt.tempos_iteracoes is None
        assert nt.versao_modelo is None
        assert nt.biblioteca_pl is None
        assert nt.caso is None
        assert nt.data_hora_inicio is None
        assert nt.data_hora_inicio_politica is None
        assert nt.numero_processos is None
        assert nt.numero_nos is None
        assert nt.tipo_execucao is None
        assert nt.iteracoes_minimo is None
        assert nt.iteracoes_maximo is None


def test_eq_newavetim():
    m: MagicMock = mock_open(read_data="".join(MockNewaveTim))
    with patch("builtins.open", m):
        nt1 = Newavetim.read(ARQ_TESTE)
        nt2 = Newavetim.read(ARQ_TESTE)
        assert nt1 == nt2


def test_neq_newavetim():
    m: MagicMock = mock_open(read_data="".join(MockNewaveTim))
    with patch("builtins.open", m):
        nt1 = Newavetim.read(ARQ_TESTE)
        nt2 = Newavetim.read(ARQ_TESTE)
        nt2.tempos_etapas.iloc[0, 0] = ""
        assert nt1 != nt2


def _verifica_tempos_completos(linhas: list[str], versao: str):
    m: MagicMock = mock_open(read_data="".join(linhas))
    with patch("builtins.open", m):
        nt = Newavetim.read(ARQ_TESTE)

    etapas = nt.tempos_etapas
    assert etapas is not None
    assert etapas.shape[0] == 5
    tempos = nt.tempos_iteracoes
    assert tempos is not None
    assert tempos["iteracao"].tolist() == list(range(1, 51))
    politica = etapas.loc[etapas["etapa"] == "Calculo da Politica", "tempo"]
    assert tempos["total"].sum() == politica.iloc[0]
    assert (tempos["backward"] + tempos["forward"] == tempos["total"]).all()
    assert nt.versao_modelo == versao


def test_tempos_3004():
    _verifica_tempos_completos(MockNewaveTim3004, "30.0.4")


def test_tempos_3102():
    _verifica_tempos_completos(MockNewaveTim3102, "31.0.2_centos")


def test_tempos_315():
    _verifica_tempos_completos(MockNewaveTim315, "31.5_COIN_FT")


# NOTE: Output-only file, round-trip test not applicable


PROPRIEDADES_CABECALHO = [
    "versao_modelo",
    "biblioteca_pl",
    "caso",
    "data_hora_inicio",
    "data_hora_inicio_politica",
    "numero_processos",
    "numero_nos",
    "tipo_execucao",
    "iteracoes_minimo",
    "iteracoes_maximo",
]


def _le_cabecalho(linhas: list[str]) -> dict[str, Any]:
    m: MagicMock = mock_open(read_data="".join(linhas))
    with patch("builtins.open", m):
        nt = Newavetim.read(ARQ_TESTE)
    return {p: getattr(nt, p) for p in PROPRIEDADES_CABECALHO}


def test_cabecalho_3004():
    assert _le_cabecalho(MockNewaveTim3004) == {
        "versao_modelo": "30.0.4",
        "biblioteca_pl": "COIN  Versao 1.16",
        "caso": "caso de teste",
        "data_hora_inicio": datetime(2026, 11, 3, 1, 15, 40, 46000),
        "data_hora_inicio_politica": None,
        "numero_processos": 200,
        "numero_nos": 3,
        "tipo_execucao": "Politica e Simulacao Final",
        "iteracoes_minimo": 50,
        "iteracoes_maximo": 50,
    }


def test_cabecalho_3102():
    assert _le_cabecalho(MockNewaveTim3102) == {
        "versao_modelo": "31.0.2_centos",
        "biblioteca_pl": "COIN  Versao 1.16",
        "caso": "caso de teste",
        "data_hora_inicio": datetime(2026, 10, 30, 1, 12, 36, 955000),
        "data_hora_inicio_politica": None,
        "numero_processos": 200,
        "numero_nos": 3,
        "tipo_execucao": "Politica e Simulacao Final",
        "iteracoes_minimo": 50,
        "iteracoes_maximo": 50,
    }


def test_cabecalho_315():
    assert _le_cabecalho(MockNewaveTim315) == {
        "versao_modelo": "31.5_COIN_FT",
        "biblioteca_pl": "COIN versao 1.16",
        "caso": "caso de teste",
        "data_hora_inicio": datetime(2026, 9, 9, 17, 45, 50, 396000),
        "data_hora_inicio_politica": datetime(2026, 9, 9, 18, 0, 15, 188000),
        "numero_processos": 64,
        "numero_nos": 1,
        "tipo_execucao": "Politica e Simulacao Final",
        "iteracoes_minimo": 50,
        "iteracoes_maximo": 50,
    }


def test_cabecalho_2863():
    assert _le_cabecalho(MockNewaveTim) == {
        "versao_modelo": "28.6.3_CPAMP",
        "biblioteca_pl": None,
        "caso": "PMO MARCO - 2020  27/2/2020 13:13:47  Niveis para 29/02 NW Versao 27",
        "data_hora_inicio": datetime(2022, 8, 13, 11, 1, 8, 429000),
        "data_hora_inicio_politica": None,
        "numero_processos": 72,
        "numero_nos": 9,
        "tipo_execucao": "Politica e Simulacao Final",
        "iteracoes_minimo": 30,
        "iteracoes_maximo": 50,
    }


def test_cabecalho_so_versao():
    assert _le_cabecalho(MockBlocoVersaoModelo) == {
        "versao_modelo": "28.6.3_CPAMP",
        "biblioteca_pl": None,
        "caso": None,
        "data_hora_inicio": None,
        "data_hora_inicio_politica": None,
        "numero_processos": None,
        "numero_nos": None,
        "tipo_execucao": None,
        "iteracoes_minimo": None,
        "iteracoes_maximo": None,
    }


def test_cabecalho_ilegivel():
    linhas = [
        "Numero de Processos:   xx\n"
        if linha.startswith("Numero de Processos:")
        else linha
        for linha in MockNewaveTim
    ]
    m: MagicMock = mock_open(read_data="".join(linhas))
    with patch("builtins.open", m):
        with pytest.raises(ValueError, match="numero_processos"):
            Newavetim.read(ARQ_TESTE)
