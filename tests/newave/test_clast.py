# Rotinas de testes associadas ao arquivo clast.dat do NEWAVE
from inewave.newave.modelos.clast import BlocoUTEClasT
from inewave.newave.modelos.clast import BlocoModificacaoUTEClasT

from inewave.newave import Clast


from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.clast import MockBlocoUTEClasT
from tests.mocks.arquivos.clast import MockBlocoModificacaoClasT
from tests.mocks.arquivos.clast import MockClasT
from tests.mocks.arquivos.clast import MockBlocoUTEClasT4Anos
from tests.mocks.arquivos.clast import MockBlocoUTEClasT6Anos

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_ute_clast():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUTEClasT))
    b = BlocoUTEClasT()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 1
    assert b.data.iloc[-1, -1] == 0.0


def test_atributos_encontrados_ute_clast():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUTEClasT))
    with patch("builtins.open", m):
        ct = Clast.read(ARQ_TESTE)
        assert ct.usinas is not None


def test_atributos_nao_encontrados_ute_clast():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ct = Clast.read(ARQ_TESTE)
        assert ct.usinas is None


def test_bloco_modificacao_clast():
    m: MagicMock = mock_open(read_data="".join(MockBlocoModificacaoClasT))
    b = BlocoModificacaoUTEClasT()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert b.data.iloc[0, 0] == 211
    assert b.data.iloc[-1, -1] == 178.25


def test_atributos_encontrados_modificacao_clast():
    m: MagicMock = mock_open(read_data="".join(MockClasT))
    with patch("builtins.open", m):
        ct = Clast.read(ARQ_TESTE)
        assert ct.modificacoes is not None


def test_atributos_nao_encontrados_modificacao_clast():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ct = Clast.read(ARQ_TESTE)
        assert ct.modificacoes is None


def test_eq_clast():
    m: MagicMock = mock_open(read_data="".join(MockClasT))
    with patch("builtins.open", m):
        ct1 = Clast.read(ARQ_TESTE)
        ct2 = Clast.read(ARQ_TESTE)
        assert ct1 == ct2


def test_neq_cadic():
    m: MagicMock = mock_open(read_data="".join(MockClasT))
    with patch("builtins.open", m):
        ct1 = Clast.read(ARQ_TESTE)
        ct2 = Clast.read(ARQ_TESTE)
        ct2.usinas.iloc[0, 0] = -1
        assert ct1 != ct2


def test_leitura_escrita_clast():
    m_leitura: MagicMock = mock_open(read_data="".join(MockClasT))
    with patch("builtins.open", m_leitura):
        ct1 = Clast.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ct1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        ct2 = Clast.read(ARQ_TESTE)
        assert ct1 == ct2


def test_tipo_combustivel_nao_invade_campo_custo():
    # Usinas com CVU >= 1000 tinham o primeiro digito do custo capturado
    # pelo campo de combustivel (largura 12 em vez de 10).
    m: MagicMock = mock_open(read_data="".join(MockBlocoUTEClasT))
    with patch("builtins.open", m):
        ct = Clast.read(ARQ_TESTE)

    combustiveis = set(ct.usinas["tipo_combustivel"].unique())
    assert all(not c.strip()[-1].isdigit() for c in combustiveis)

    daia = ct.usinas.loc[ct.usinas["codigo_usina"] == 153]
    assert daia["tipo_combustivel"].iloc[0].strip() == "Diesel"
    assert daia["valor"].iloc[0] == 1178.85


def test_leitura_clast_4_colunas_custo():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUTEClasT4Anos))
    with patch("builtins.open", m):
        ct = Clast.read(ARQ_TESTE)

    assert sorted(ct.usinas["indice_ano_estudo"].unique()) == [1, 2, 3, 4]
    assert not ct.usinas["valor"].isna().any()
    angra = ct.usinas.loc[ct.usinas["codigo_usina"] == 1]
    assert angra["valor"].tolist() == [31.17, 31.17, 31.17, 31.17]


def test_leitura_clast_6_colunas_custo():
    m: MagicMock = mock_open(read_data="".join(MockBlocoUTEClasT6Anos))
    with patch("builtins.open", m):
        ct = Clast.read(ARQ_TESTE)

    assert sorted(ct.usinas["indice_ano_estudo"].unique()) == [1, 2, 3, 4, 5, 6]
    campo = ct.usinas.loc[ct.usinas["codigo_usina"] == 491]
    assert campo["valor"].tolist() == [
        1314.04,
        1053.57,
        949.33,
        904.59,
        904.59,
        904.59,
    ]


def test_leitura_escrita_clast_4_colunas_custo():
    # O bloco de modificacoes e concatenado porque Clast.write() percorre
    # todas as secoes do arquivo (BlocoUTEClasT e BlocoModificacaoUTEClasT);
    # sem dados de modificacao, BlocoModificacaoUTEClasT.write() levanta
    # ValueError - convencao ja existente na biblioteca, independente
    # do numero de colunas de custo testado aqui.
    m_leitura: MagicMock = mock_open(
        read_data="".join(MockBlocoUTEClasT4Anos + MockBlocoModificacaoClasT)
    )
    with patch("builtins.open", m_leitura):
        ct1 = Clast.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ct1.write(ARQ_TESTE)
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    # o cabecalho preservado nao deve ganhar colunas de custo extras
    assert linhas_escritas[1].count("XXXX.XX") == 4


def test_escrita_clast_ajusta_cabecalho_ao_estender_horizonte():
    # Ao acrescentar um ano ao DataFrame, o cabecalho precisa ganhar a
    # coluna correspondente, senao a releitura trunca de volta.
    import pandas as pd

    # Idem: bloco de modificacoes concatenado para que Clast.write() nao
    # levante ValueError na secao sem dados (ver comentario no teste
    # anterior).
    m_leitura: MagicMock = mock_open(
        read_data="".join(MockBlocoUTEClasT4Anos + MockBlocoModificacaoClasT)
    )
    with patch("builtins.open", m_leitura):
        ct1 = Clast.read(ARQ_TESTE)

    df = ct1.usinas
    ano_extra = df.loc[df["indice_ano_estudo"] == 4].copy()
    ano_extra["indice_ano_estudo"] = 5
    ct1.usinas = pd.concat([df, ano_extra], ignore_index=True)

    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ct1.write(ARQ_TESTE)
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    assert linhas_escritas[0].count("CUSTO") == 5
    assert linhas_escritas[1].count("XXXX.XX") == 5
