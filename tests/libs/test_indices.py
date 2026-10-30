import inspect

from cfinterface.components.register import Register

import inewave.libs.modelos.indices as modelos_indices
from inewave.libs import Indices
from inewave.libs.modelos.indices import RegistroIndice
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.indices import (
    MockIndices,
    MockIndicesLinhaCurta,
    MockIndicesNewave,
    MockIndicesRepetidos,
    MockRegistroIndice,
    MockRegistroIndiceCampoVazio,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_registro_indice():
    m: MagicMock = mock_open(read_data="".join(MockRegistroIndice))
    r = RegistroIndice()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [
        "RESTRICAO-ELETRICA-ESPECIAL",
        "Dados da funcionalidade restricao-eletrica-especial",
        "lib_restricao-eletrica-especial.csv",
    ]
    assert r.identificador == "RESTRICAO-ELETRICA-ESPECIAL"
    r.identificador = "RESTRICAO-ELETRICA-VIOLACAO"
    assert r.identificador == "RESTRICAO-ELETRICA-VIOLACAO"
    assert r.descricao == "Dados da funcionalidade restricao-eletrica-especial"
    r.descricao = ""
    assert r.descricao == ""
    assert r.arquivo == "lib_restricao-eletrica-especial.csv"
    r.arquivo = "restricoes.csv"
    assert r.arquivo == "restricoes.csv"


def test_registro_indice_campo_vazio():
    m: MagicMock = mock_open(read_data="".join(MockRegistroIndiceCampoVazio))
    r = RegistroIndice()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [
        "RESTRICAO-ELETRICA-ESPECIAL",
        "",
        "restricao-eletrica.csv",
    ]


def test_matches_registro_indice():
    assert RegistroIndice.matches(" PARQUE-EOLICO-EQUIVALENTE ; ; a.csv\n")
    assert RegistroIndice.matches(b"PARQUE-EOLICO-EQUIVALENTE;;a.csv\n")
    assert not RegistroIndice.matches("&ID;Descricao;Caminho\n")
    assert not RegistroIndice.matches("   & ID;Descricao;Caminho\n")
    assert not RegistroIndice.matches(b"&ID;Descricao;Caminho\n")
    assert not RegistroIndice.matches("PARQUE-EOLICO-EQUIVALENTE\n")
    assert not RegistroIndice.matches("\n")


def test_atributos_encontrados_indices():
    m: MagicMock = mock_open(read_data="".join(MockIndices))
    with patch("builtins.open", m):
        indices = Indices.read(ARQ_TESTE)
        assert indices.indices() is not None


def test_atributos_nao_encontrados_indices():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        indices = Indices.read(ARQ_TESTE)
        assert indices.indices() is None
        assert indices.indices(df=True).empty


def test_df_indices():
    m: MagicMock = mock_open(read_data="".join(MockIndices))
    with patch("builtins.open", m):
        indices = Indices.read(ARQ_TESTE)
        df = indices.indices(df=True)
        assert list(df.columns) == ["arquivo", "descricao", "identificador"]
        assert df["identificador"].tolist() == [
            "HIDRELETRICA-CADASTRO-RESERVATORIO-CURVAJUSANTE",
            "PARQUE-EOLICO-EQUIVALENTE-CADASTRO",
            "PARQUE-EOLICO-EQUIVALENTE-CONFIGURACAO",
            "PARQUE-EOLICO-EQUIVALENTE-SUBMERCADO",
            "RESTRICAO-ELETRICA-ESPECIAL",
            "HIDRELETRICA-CADASTRO-RESERVATORIO",
        ]
        assert df["arquivo"].tolist() == [
            "polinjus.csv",
            "renovaveis.csv",
            "renovaveis.csv",
            "renovaveis.csv",
            "lib_restricao-eletrica-especial.csv",
            "volumes-referencia.csv",
        ]
        assert df.at[0, "descricao"] == "pol"
        assert df.at[5, "descricao"] == ""


def test_filtros_indices():
    m: MagicMock = mock_open(read_data="".join(MockIndices))
    with patch("builtins.open", m):
        indices = Indices.read(ARQ_TESTE)
        r = indices.indices("HIDRELETRICA-CADASTRO-RESERVATORIO")
        assert isinstance(r, RegistroIndice)
        assert r.arquivo == "volumes-referencia.csv"
        renovaveis = indices.indices(arquivo="renovaveis.csv")
        assert isinstance(renovaveis, list)
        assert len(renovaveis) == 3
        assert (
            indices.indices("HIDRELETRICA-FPHA-METODO-REDUCAO-CORTES") is None
        )


def test_identificadores_repetidos_indices():
    m: MagicMock = mock_open(read_data="".join(MockIndicesRepetidos))
    with patch("builtins.open", m):
        indices = Indices.read(ARQ_TESTE)
        repetidos = indices.indices("RESTRICAO-ELETRICA-ESPECIAL")
        assert isinstance(repetidos, list)
        assert [r.arquivo for r in repetidos] == [
            "restricao-eletrica.csv",
            "restricao-eletrica-3.csv",
        ]
        minusculo = indices.indices("restricao-eletrica-especial")
        assert isinstance(minusculo, RegistroIndice)
        assert minusculo.arquivo == "restricao-eletrica-2.csv"


def test_indices_caso_newave_crlf_e_card_comentado():
    m: MagicMock = mock_open(read_data="".join(MockIndicesNewave))
    with patch("builtins.open", m):
        arq = Indices.read(ARQ_TESTE)
    df = arq.indices(df=True)
    assert df["identificador"].tolist() == [
        "RESTRICAO-ELETRICA-ESPECIAL",
        "HIDRELETRICA-CADASTRO-RESERVATORIO-CURVAJUSANTE",
        "HIDRELETRICA-CADASTRO-RESERVATORIO",
    ]
    assert df["descricao"].tolist() == ["", "", ""]
    assert df["arquivo"].tolist() == [
        "restricao-eletrica.csv",
        "polinjus.csv",
        "volumes-referencia.csv",
    ]
    # O card comentado não é um registro de índice
    assert (
        arq.indices(identificador="HIDRELETRICA-FPHA-METODO-REDUCAO-CORTES")
        is None
    )


def test_linha_curta_indices():
    m: MagicMock = mock_open(read_data="".join(MockIndicesLinhaCurta))
    with patch("builtins.open", m):
        indices = Indices.read(ARQ_TESTE)
        curta = indices.indices("RESTRICAO-ELETRICA-ESPECIAL")
        assert isinstance(curta, RegistroIndice)
        assert curta.descricao == "Restricoes"
        assert curta.arquivo is None


def test_eq_indices():
    m: MagicMock = mock_open(read_data="".join(MockIndices))
    with patch("builtins.open", m):
        cf1 = Indices.read(ARQ_TESTE)
        cf2 = Indices.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_indices():
    m: MagicMock = mock_open(read_data="".join(MockIndices))
    with patch("builtins.open", m):
        cf1 = Indices.read(ARQ_TESTE)
        cf2 = Indices.read(ARQ_TESTE)
        cf2.indices()[0].arquivo = "outro.csv"
        assert cf1 != cf2


def test_leitura_escrita_indices():
    m_leitura: MagicMock = mock_open(read_data="".join(MockIndices))
    with patch("builtins.open", m_leitura):
        cf1 = Indices.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        cf1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    # Comentários são mantidos e registros são reescritos sem espaços
    escrito = "".join(linhas_escritas).splitlines(keepends=True)
    assert len(escrito) == len(MockIndices)
    assert escrito[:7] == MockIndices[:7]
    assert escrito[7] == (
        "HIDRELETRICA-CADASTRO-RESERVATORIO-CURVAJUSANTE;pol;polinjus.csv\n"
    )
    assert escrito[12] == (
        "HIDRELETRICA-CADASTRO-RESERVATORIO;;volumes-referencia.csv\n"
    )
    assert escrito[13] == MockIndices[13]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        cf2 = Indices.read(ARQ_TESTE)
        assert cf1 == cf2


def test_registros_modelados_indices():
    # Todo registro modelado precisa estar em REGISTERS para ser lido
    registros = [
        c
        for _, c in inspect.getmembers(modelos_indices, inspect.isclass)
        if issubclass(c, Register) and c.__module__ == modelos_indices.__name__
    ]
    assert [r for r in registros if r not in Indices.REGISTERS] == []
