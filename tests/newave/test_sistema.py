# Rotinas de testes associadas ao arquivo sistema.dat do NEWAVE
import io
import re
from typing import List

from inewave.newave.modelos.sistema import (
    BlocoNumeroPatamaresDeficit,
    BlocoCustosDeficit,
    BlocoIntercambioSubsistema,
    BlocoMercadoEnergiaSistema,
    BlocoGeracaoUsinasNaoSimuladas,
)

from inewave.newave import Sistema


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.sistema import (
    MockBlocoNumeroPatamaresDeficit,
    MockBlocoCustoDeficit,
    MockBlocoLimitesIntercambio,
    MockBlocoMercadoEnergia,
    MockBlocoGeracaoUsinasNaoSimuladas,
    MockSistema,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_numero_patamares_deficit_sistema():
    m: MagicMock = mock_open(read_data="".join(MockBlocoNumeroPatamaresDeficit))
    b = BlocoNumeroPatamaresDeficit()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data == 1


def test_bloco_custos_deficit_sistema():
    m: MagicMock = mock_open(read_data="".join(MockBlocoCustoDeficit))
    b = BlocoCustosDeficit()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, 0] == 11
    assert b.data.iloc[0, 4] == 6524.05


def test_bloco_limites_intercambio_sistema():
    m: MagicMock = mock_open(read_data="".join(MockBlocoLimitesIntercambio))
    b = BlocoIntercambioSubsistema()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 7500.0


def test_bloco_mercado_energia_sistema():
    m: MagicMock = mock_open(read_data="".join(MockBlocoMercadoEnergia))
    b = BlocoMercadoEnergiaSistema()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 6657.0


def test_bloco_usinas_nao_simuladas_sistema():
    m: MagicMock = mock_open(
        read_data="".join(MockBlocoGeracaoUsinasNaoSimuladas)
    )
    b = BlocoGeracaoUsinasNaoSimuladas()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 1.0


def test_atributos_encontrados_sistema():
    m: MagicMock = mock_open(read_data="".join(MockSistema))
    with patch("builtins.open", m):
        ad = Sistema.read(ARQ_TESTE)
        assert ad.numero_patamares_deficit is not None
        assert ad.custo_deficit is not None
        assert ad.limites_intercambio is not None
        assert ad.mercado_energia is not None
        assert ad.geracao_usinas_nao_simuladas is not None


def test_atributos_nao_encontrados_sistema():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ad = Sistema.read(ARQ_TESTE)
        assert ad.numero_patamares_deficit is None
        assert ad.custo_deficit is None
        assert ad.limites_intercambio is None
        assert ad.mercado_energia is None
        assert ad.geracao_usinas_nao_simuladas is None


def test_eq_sistema():
    m: MagicMock = mock_open(read_data="".join(MockSistema))
    with patch("builtins.open", m):
        cf1 = Sistema.read(ARQ_TESTE)
        cf2 = Sistema.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_sistema():
    m: MagicMock = mock_open(read_data="".join(MockSistema))
    with patch("builtins.open", m):
        cf1 = Sistema.read(ARQ_TESTE)
        cf2 = Sistema.read(ARQ_TESTE)
        cf2.numero_patamares_deficit = 0
        assert cf1 != cf2


def test_leitura_escrita_sistema():
    m_leitura: MagicMock = mock_open(read_data="".join(MockSistema))
    with patch("builtins.open", m_leitura):
        cf1 = Sistema.read(ARQ_TESTE)
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
        cf2 = Sistema.read(ARQ_TESTE)
        assert cf1 == cf2


def test_escrita_intercambio_usa_registro_em_branco():
    # Manual do NEWAVE v30.0.2, secao 3.7, Bloco 3: os grupos de registros
    # tipo 2 (A->B) e tipo 3 (B->A) sao "separados por um registro em
    # branco, de existencia obrigatoria". O cabecalho tipo 1 nao deve ser
    # repetido nessa virada.
    m_leitura: MagicMock = mock_open(read_data="".join(MockSistema))
    with patch("builtins.open", m_leitura):
        sist = Sistema.read(ARQ_TESTE)

    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        sist.write(ARQ_TESTE)
        chamadas = m_escrita.mock_calls
        linhas = [chamadas[i].args[0] for i in range(1, len(chamadas) - 1)]

    # Um cabecalho tipo 1 por par de submercados, nao um por sentido.
    cabecalhos = [
        line for line in linhas if re.match(r"^\s*\d+\s+\d+\s+\d\s*$", line)
    ]
    pares = [tuple(line.split()[:2]) for line in cabecalhos]
    assert len(pares) == len(set(pares)), (
        f"cabecalho tipo 1 repetido para o mesmo par: {pares}"
    )

    # E deve existir ao menos um registro em branco separando os grupos.
    assert any(line == "\n" for line in linhas)


def test_bloco_intercambio_flag_e_sentido():
    # A coluna `flag` (campo 3 do registro tipo 1: 0 = limite,
    # 1 = intercâmbio mínimo obrigatório) é exposta sem alterar o `sentido`
    # histórico. Este deck só tem limites, então flag == 0 em todo lugar.
    m: MagicMock = mock_open(read_data="".join(MockBlocoLimitesIntercambio))
    b = BlocoIntercambioSubsistema()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    df = b.data
    assert "flag" in df.columns
    assert set(df["flag"].unique()) == {0}
    # sentido preservado: no par (1, 2) o grupo A->B (10280) tem sentido 0 e
    # o grupo B->A (6694) tem sentido 1, exatamente como antes da mudança.
    p12 = df[(df["submercado_de"] == 1) & (df["submercado_para"] == 2)]
    assert set(p12[p12["valor"] == 10280.0]["sentido"]) == {0}
    assert set(p12[p12["valor"] == 6694.0]["sentido"]) == {1}


def _le_bloco_intercambio(linhas: List[str]) -> BlocoIntercambioSubsistema:
    b = BlocoIntercambioSubsistema()
    b.read(io.StringIO("".join(linhas)))
    return b


def _escreve_bloco_intercambio(b: BlocoIntercambioSubsistema) -> str:
    buf = io.StringIO()
    b.write(buf)
    return buf.getvalue()


def _com_cabecalho_repetido(linhas: List[str]) -> List[str]:
    # Leiaute escrito pelo inewave até a v1.14: no lugar do registro em
    # branco, o registro tipo 1 do par é repetido com o campo 3 igual a 1.
    saida: List[str] = []
    par = ""
    for linha in linhas:
        if re.match(r"^\s+\d+\s+\d+\s+\d\s*$", linha):
            par = linha[:8]
        saida.append(par + " " * 15 + "1\n" if linha == "\n" else linha)
    return saida


def test_bloco_intercambio_cabecalho_repetido_separa_os_sentidos():
    linhas = _com_cabecalho_repetido(MockBlocoLimitesIntercambio)
    assert "   1   2               1\n" in linhas
    assert "\n" not in linhas
    antigo = _le_bloco_intercambio(linhas)
    atual = _le_bloco_intercambio(MockBlocoLimitesIntercambio)

    # O registro repetido só separa os sentidos: não é um registro de
    # intercâmbio mínimo obrigatório.
    assert set(antigo.data["flag"]) == {0}
    assert antigo == atual
    p12 = antigo.data[
        (antigo.data["submercado_de"] == 1)
        & (antigo.data["submercado_para"] == 2)
    ]
    assert set(p12[p12["valor"] == 10280.0]["sentido"]) == {0}
    assert set(p12[p12["valor"] == 6694.0]["sentido"]) == {1}

    # A escrita segue o manual, com o registro em branco entre os grupos.
    assert _escreve_bloco_intercambio(antigo) == _escreve_bloco_intercambio(
        atual
    )


def _grupo_intercambio(valor: int) -> List[str]:
    return [
        f"{ano}    " + "  ".join(f"{valor:>6}" for _ in range(12)) + "\n"
        for ano in (2021, 2022)
    ]


MockBlocoParLimiteEMinimo = (
    MockBlocoLimitesIntercambio[:3]
    + ["   1   2               0\n"]
    + _grupo_intercambio(1000)
    + ["\n"]
    + _grupo_intercambio(2000)
    + ["   1   2               1\n"]
    + _grupo_intercambio(300)
    + ["\n"]
    + _grupo_intercambio(0)
    + [" 999\n"]
)


def test_bloco_intercambio_par_com_limite_e_minimo():
    # Manual do NEWAVE, seção 3.7, Bloco 3: o intercâmbio mínimo
    # obrigatório não pode superar o limite da interligação, então o par
    # tem um registro de limite (campo 3 = 0) e outro de mínimo (campo 3 =
    # 1), cada um com os grupos A->B e B->A.
    b = _le_bloco_intercambio(MockBlocoParLimiteEMinimo)
    df = b.data.copy()
    df["direcao"] = df["sentido"] ^ df["flag"]
    valores = df.groupby(["flag", "direcao"])["valor"].unique()
    assert valores.loc[(0, 0)].tolist() == [1000.0]
    assert valores.loc[(0, 1)].tolist() == [2000.0]
    assert valores.loc[(1, 0)].tolist() == [300.0]
    assert valores.loc[(1, 1)].tolist() == [0.0]

    # Cada registro é escrito inteiro, sem misturar os valores do par.
    saida = _escreve_bloco_intercambio(b)
    assert saida == "".join(MockBlocoParLimiteEMinimo)
    assert _le_bloco_intercambio(saida.splitlines(keepends=True)) == b


def test_bloco_intercambio_flag_minimo_roundtrip():
    # Par (1, 2) com campo 3 = 1 (intercâmbio mínimo obrigatório). O flag deve
    # ser capturado, a direção A->B/B->A (posicional) preservada e o
    # round-trip estável — cenário que a coluna única `sentido` não cobria.
    mock_flag1 = [
        linha.replace("   1   2               0", "   1   2               1")
        for linha in MockBlocoLimitesIntercambio
    ]
    m: MagicMock = mock_open(read_data="".join(mock_flag1))
    b = BlocoIntercambioSubsistema()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    df = b.data
    p12 = df[(df["submercado_de"] == 1) & (df["submercado_para"] == 2)]
    assert set(p12["flag"]) == {1}
    # os demais pares continuam com flag 0
    outros = df[(df["submercado_de"] != 1) | (df["submercado_para"] != 2)]
    assert set(outros["flag"]) == {0}

    # Escrita: campo 3 = 1 e grupo A->B (10280) antes do B->A (6694).
    buf = io.StringIO()
    b.write(buf)
    saida = buf.getvalue()
    assert "   1   2               1" in saida
    assert 0 < saida.find("10280") < saida.find("6694")

    # Round-trip estável: reler a saída reproduz o mesmo DataFrame.
    b2 = BlocoIntercambioSubsistema()
    b2.read(io.StringIO(saida))
    colunas = list(df.columns)
    assert (
        df.sort_values(colunas)
        .reset_index(drop=True)
        .equals(b2.data.sort_values(colunas).reset_index(drop=True))
    )
