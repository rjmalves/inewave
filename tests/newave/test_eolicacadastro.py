# Rotinas de testes associadas ao arquivo eolica-cadastro.csv do NEWAVE
from datetime import datetime
from inewave.newave.modelos.eolicacadastro import (
    RegistroEolicaCadastro,
    RegistroEolicaCadastroConjuntoAerogeradores,
    RegistroEolicaCadastroAerogerador,
    RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo,
    RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva,
    RegistroPEECadastro,
    RegistroPEEPotenciaInstaladaPeriodo,
)

from inewave.newave import EolicaCadastro

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eolicacadastro import (
    MockRegistroEolicaCadastro,
    MockRegistroEolicaCadastroAerogerador,
    MockRegistroEolicaCadastroConjuntoAerogeradores,
    MockRegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo,
    MockRegistroEolicaConjuntoAerogeradoresPotenciaEfetiva,
    MockRegistroPEECadastro,
    MockRegistroPEEPotenciaInstaladaPeriodo,
    MockEolicaCadastro,
)


def test_registro_eolica_cadastro_eolicacadastro():

    m: MagicMock = mock_open(read_data="".join(MockRegistroEolicaCadastro))
    r = RegistroEolicaCadastro()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, "NEInterior", "", 1]
    assert r.codigo_eolica == 1
    r.codigo_eolica = 5
    assert r.nome_eolica == "NEInterior"
    r.nome_eolica = "Teste"
    assert r.identificador_eolica == ""
    r.identificador_eolica = "   "
    assert r.quantidade_conjuntos == 1
    r.quantidade_conjuntos = 5


def test_registro_cadastro_aerogerador_eolicacadastro():

    m: MagicMock = mock_open(
        read_data="".join(MockRegistroEolicaCadastroAerogerador)
    )
    r = RegistroEolicaCadastroAerogerador()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, 1, 0, 0, 0, 0, 6058.890, 0, 0]
    assert r.codigo_eolica == 1
    r.codigo_eolica = 2
    assert r.indice_conjunto == 1
    r.indice_conjunto = 1
    assert r.velocidade_cutin == 0
    r.velocidade_cutin = 5
    assert r.velocidade_nominal == 0
    r.velocidade_nominal = 3
    assert r.velocidade_cutout == 0
    r.velocidade_cutout = 10
    assert r.potencia_velocidade_cutin == 0
    r.potencia_velocidade_cutin = 56
    assert r.potencia_velocidade_nominal == 6058.890
    r.potencia_velocidade_nominal = 600
    assert r.potencia_velocidade_cutout == 0
    r.potencia_velocidade_cutout = 10000
    assert r.altura_torre == 0
    r.altura_torre = 100


def test_registro_cadastro_conjunto_eolicacadastro():

    m: MagicMock = mock_open(
        read_data="".join(MockRegistroEolicaCadastroConjuntoAerogeradores)
    )
    r = RegistroEolicaCadastroConjuntoAerogeradores()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, 1, "NEInterior_cj", 1]
    assert r.codigo_eolica == 1
    r.codigo_eolica = 2
    assert r.indice_conjunto == 1
    r.indice_conjunto = 1
    assert r.nome_conjunto == "NEInterior_cj"
    r.nome_conjunto = "Teste"
    assert r.quantidade_aerogeradores == 1
    r.quantidade_aerogeradores = 2


def test_registro_cadastro_operacao_eolicacadastro():

    m: MagicMock = mock_open(
        read_data="".join(
            MockRegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo
        )
    )
    r = RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, 1, datetime(2021, 1, 1), datetime(2030, 12, 1), 1]
    assert r.codigo_eolica == 1
    r.codigo_eolica = 2
    assert r.indice_conjunto == 1
    r.indice_conjunto = 1
    assert r.periodo_inicial == datetime(2021, 1, 1)
    r.periodo_inicial = datetime(2024, 1, 1)
    assert r.periodo_final == datetime(2030, 12, 1)
    r.periodo_final = datetime(2025, 12, 1)
    assert r.numero_aerogeradores == 1
    r.numero_aerogeradores = 3


def test_registro_potenciaefetiva_eolicacadastro():

    m: MagicMock = mock_open(
        read_data="".join(
            MockRegistroEolicaConjuntoAerogeradoresPotenciaEfetiva
        )
    )
    r = RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [
        1,
        1,
        datetime(2021, 1, 1),
        datetime(2030, 12, 1),
        6058.890,
    ]
    assert r.codigo_eolica == 1
    r.codigo_eolica = 2
    assert r.indice_conjunto == 1
    r.indice_conjunto = 1
    assert r.periodo_inicial == datetime(2021, 1, 1)
    r.periodo_inicial = datetime(2024, 1, 1)
    assert r.periodo_final == datetime(2030, 12, 1)
    r.periodo_final = datetime(2025, 12, 1)
    assert r.potencia_efetiva == 6058.890
    r.potencia_efetiva = 5


def test_registro_pee_cadastro():

    m: MagicMock = mock_open(read_data="".join(MockRegistroPEECadastro))
    r = RegistroPEECadastro()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, "NEInterior"]
    assert r.codigo_pee == 1
    r.codigo_pee = 2
    assert r.nome_pee == "NEInterior"
    r.nome_pee = "NEInterior"


def test_registro_pee_potencia_instalada_periodo():

    m: MagicMock = mock_open(
        read_data="".join(MockRegistroPEEPotenciaInstaladaPeriodo)
    )
    r = RegistroPEEPotenciaInstaladaPeriodo()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [
        1,
        datetime(year=2021, month=1, day=1),
        datetime(year=2030, month=12, day=1),
        6058.890,
    ]
    assert r.codigo_pee == 1
    r.codigo_pee = 2
    assert r.periodo_inicial == datetime(year=2021, month=1, day=1)
    r.periodo_inicial = datetime(year=2021, month=2, day=1)
    assert r.periodo_final == datetime(year=2030, month=12, day=1)
    r.periodo_final = datetime(year=2021, month=2, day=1)
    assert r.potencia_instalada == 6058.89
    r.potencia_instalada = 1000.0


def test_atributos_encontrados_eolicacadastro():
    m: MagicMock = mock_open(read_data="".join(MockEolicaCadastro))
    with patch("builtins.open", m):
        e = EolicaCadastro.le_arquivo("")
        assert len(e.eolica_cadastro()) > 0
        assert len(e.eolica_cadastro_aerogerador()) > 0
        assert len(e.eolica_cadastro_conjunto_aerogeradores()) > 0
        assert (
            len(e.eolica_conjunto_aerogeradores_quantidade_operando_periodo())
            > 0
        )
        assert (
            len(e.eolica_conjunto_aerogeradores_potencia_efetiva_periodo()) > 0
        )


def test_eq_eolicacadastro():
    m: MagicMock = mock_open(read_data="".join(MockEolicaCadastro))
    with patch("builtins.open", m):
        cf1 = EolicaCadastro.le_arquivo("")
        cf2 = EolicaCadastro.le_arquivo("")
        assert cf1 == cf2


def test_neq_eolicacadastro():
    m: MagicMock = mock_open(read_data="".join(MockEolicaCadastro))
    with patch("builtins.open", m):
        cf1 = EolicaCadastro.le_arquivo("")
        cf2 = EolicaCadastro.le_arquivo("")
        cf2.deleta_registro(cf1.eolica_cadastro()[0])
        assert cf1 != cf2


def test_leitura_escrita_eolicacadastro():
    m_leitura: MagicMock = mock_open(read_data="".join(MockEolicaCadastro))
    with patch("builtins.open", m_leitura):
        cf1 = EolicaCadastro.le_arquivo("")
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        cf1.escreve_arquivo("", "")
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(2, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        cf2 = EolicaCadastro.le_arquivo("")
        assert cf1 == cf2
