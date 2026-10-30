# Rotinas de testes associadas ao arquivo agrint.dat do NEWAVE
import io
from typing import List

import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package

from inewave.newave.modelos.agrint import (
    BlocoGruposAgrint,
    BlocoLimitesPorGrupoAgrint,
)

from inewave.newave import Agrint


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.agrint import (
    MockBlocoGruposAgrint,
    MockBlocoLimitesPorGrupoAgrint,
    MockAgrint,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_grupos_agrint():
    m: MagicMock = mock_open(read_data="".join(MockBlocoGruposAgrint))
    b = BlocoGruposAgrint()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, 0] == 14
    assert b.data.iloc[-1, 2] == 1


def test_bloco_limites_agrint():
    m: MagicMock = mock_open(read_data="".join(MockBlocoLimitesPorGrupoAgrint))
    b = BlocoLimitesPorGrupoAgrint()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, 0] == 14
    assert b.data.iloc[-1, -1] == 17923


def test_atributos_encontrados_agrint():
    m: MagicMock = mock_open(read_data="".join(MockAgrint))
    with patch("builtins.open", m):
        ad = Agrint.read(ARQ_TESTE)
        assert ad.agrupamentos is not None
        assert ad.limites_agrupamentos is not None


def test_atributos_nao_encontrados_agrint():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Agrint.read(ARQ_TESTE)
        assert ad.agrupamentos is None
        assert ad.limites_agrupamentos is None


def test_eq_agrint():
    m: MagicMock = mock_open(read_data="".join(MockAgrint))
    with patch("builtins.open", m):
        cf1 = Agrint.read(ARQ_TESTE)
        cf2 = Agrint.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_agrint():
    m: MagicMock = mock_open(read_data="".join(MockAgrint))
    with patch("builtins.open", m):
        cf1 = Agrint.read(ARQ_TESTE)
        cf2 = Agrint.read(ARQ_TESTE)
        cf2.agrupamentos.loc[0, 0] = 0
        assert cf1 != cf2


def test_leitura_escrita_agrint():
    m_leitura: MagicMock = mock_open(read_data="".join(MockAgrint))
    with patch("builtins.open", m_leitura):
        cf1 = Agrint.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        cf1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        cf2 = Agrint.read(ARQ_TESTE)
        assert cf1 == cf2


MockBlocoLimitesCincoPatamares = [
    "LIMITES POR GRUPO\n",
    "  #AG MI ANOI MF ANOF LIM_P1  LIM_P2  LIM_P3  LIM_P4  LIM_P5\n",
    " XXX  XX XXXX XX XXXX XXXXXX. XXXXXX. XXXXXX. XXXXXX. XXXXXX.\n",
    "   1   2 2023  2 2023   9000.   9100.   9200.   9300.   9400."
    "     RECEBIMENTO NE\n",
    "   2   3 2023          11000.  11100.  11200.  11300.  11400."
    "     EXPORTACAO  NE\n",
    " 999\n",
]


def _le_limites(linhas: List[str], **kwargs: int) -> BlocoLimitesPorGrupoAgrint:
    b = BlocoLimitesPorGrupoAgrint()
    b.read(io.StringIO("".join(linhas)), **kwargs)
    return b


def _escreve_limites(b: BlocoLimitesPorGrupoAgrint) -> str:
    buf = io.StringIO()
    b.write(buf)
    return buf.getvalue()


def test_bloco_limites_agrint_cinco_patamares():
    # Manual do NEWAVE, seção 3.26, Bloco 2: até 5 patamares de carga.
    b = _le_limites(MockBlocoLimitesCincoPatamares)
    df = b.data
    assert df["patamar"].tolist() == [1, 2, 3, 4, 5] * 2
    assert df["valor"].tolist()[:5] == [9000.0, 9100.0, 9200.0, 9300.0, 9400.0]
    assert df["comentario"].unique().tolist() == [
        "RECEBIMENTO NE",
        "EXPORTACAO  NE",
    ]
    assert _le_limites(
        _escreve_limites(b).splitlines(keepends=True)
    ).data.equals(df)


def test_bloco_limites_agrint_comentario_colado_aos_limites():
    # O comentário não tem coluna no manual: é lido a partir do fim dos
    # limites, sem truncar quando o arquivo não guarda o afastamento usual.
    linhas = MockBlocoLimitesCincoPatamares[:3] + [
        "   1   2 2023  2 2023   9000.   9100.   9200.   9300.   9400. LIMITE\n",
        " 999\n",
    ]
    assert _le_limites(linhas).data["comentario"].unique().tolist() == [
        "LIMITE"
    ]


def test_bloco_limites_agrint_numero_patamares_sem_template():
    # Sem colunas na linha de template, vale o argumento numero_patamares.
    linhas = [
        linha.replace(" XXXXXX.", "") if linha.startswith(" XXX") else linha
        for linha in MockBlocoLimitesCincoPatamares
    ]
    assert _le_limites(linhas, numero_patamares=5).data["patamar"].max() == 5
    assert _le_limites(linhas).data["patamar"].max() == 3


def test_escrita_limites_agrint_acompanha_numero_de_patamares():
    b = _le_limites(MockBlocoLimitesPorGrupoAgrint)
    quarto = b.data.loc[b.data["patamar"] == 3].copy()
    quarto["patamar"] = 4
    b.data = (
        pd.concat([b.data, quarto])
        .sort_values(["agrupamento", "data_inicio", "patamar"], kind="stable")
        .reset_index(drop=True)
    )
    saida = _escreve_limites(b).splitlines(keepends=True)
    assert saida[1] == (
        "  #AG MI ANOI MF ANOF LIM_P1  LIM_P2  LIM_P3  LIM_P4\n"
    )
    assert saida[2] == (
        " XXX  XX XXXX XX XXXX XXXXXX. XXXXXX. XXXXXX. XXXXXX.\n"
    )
    relido = _le_limites(saida).data
    assert relido["patamar"].max() == 4
    colunas = ["agrupamento", "data_inicio", "patamar", "valor"]
    assert relido[colunas].equals(b.data[colunas])

    # E de volta a 3 patamares, o cabeçalho volta ao original.
    b.data = b.data.loc[b.data["patamar"] <= 3].reset_index(drop=True)
    saida = _escreve_limites(b).splitlines(keepends=True)
    assert saida[:3] == MockBlocoLimitesPorGrupoAgrint[:3]
