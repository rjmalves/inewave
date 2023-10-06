# Rotinas de testes associadas ao arquivo eolica-cadastro.csv do NEWAVE
from datetime import datetime
from inewave.libs.modelos.eolica import (
    RegistroEolicaCadastro,
    RegistroEolicaCadastroConjuntoAerogeradores,
    RegistroEolicaCadastroAerogerador,
    RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo,
    RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva,
    RegistroPEECadastro,
    RegistroPEEPotenciaInstaladaPeriodo,
    RegistroEolicaConfiguracao,
    RegistroPEEConfiguracaoPeriodo,
    RegistroEolicaFTE,
    RegistroPEEFTE,
    RegistroEolicaGeracaoPatamar,
    RegistroPEEGeracaoPatamar,
    RegistroEolicaHistoricoVentoHorizonte,
    RegistroEolicaHistoricoVento,
    RegistroHistoricoVentoHorizonte,
    RegistroHistoricoVento,
    RegistroPostoVentoCadastro,
    RegistroPEEPostoVento,
    RegistroEolicaSubmercado,
    RegistroPEESubmercado,
)

from inewave.libs import Eolica

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eolica import (
    MockRegistroEolicaCadastro,
    MockRegistroEolicaCadastroAerogerador,
    MockRegistroEolicaCadastroConjuntoAerogeradores,
    MockRegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo,
    MockRegistroEolicaConjuntoAerogeradoresPotenciaEfetiva,
    MockRegistroPEECadastro,
    MockRegistroPEEPotenciaInstaladaPeriodo,
    MockEolica,
    MockRegistroEolicaConfiguracaoPeriodo,
    MockRegistroPEEConfiguracaoPeriodo,
    MockRegistroFuncaoProducao,
    MockRegistroPEEFTE,
    MockRegistroEolicaGeracaoPatamar,
    MockRegistroPEEGeracaoPatamar,
    MockRegistroEolicaHistoricoHorizonte,
    MockRegistroEolicaHistorico,
    MockRegistroHistoricoVentoHorizonte,
    MockRegistroHistoricoVento,
    MockRegistroPostoCadastro,
    MockRegistroPEEPosto,
    MockRegistroEolicaSubmercado,
    MockRegistroPEESubmercado,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_registro_eolica_cadastro():
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


def test_registro_cadastro_aerogerador():
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


def test_registro_cadastro_conjunto():
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


def test_registro_cadastro_operacao():
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


def test_registro_potenciaefetiva():
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


def test_registro_eolica_configuracao_periodo():
    m: MagicMock = mock_open(
        read_data="".join(MockRegistroEolicaConfiguracaoPeriodo)
    )
    r = RegistroEolicaConfiguracao()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [
        1,
        datetime(2021, 1, 1),
        datetime(2030, 12, 1),
        "centralizado",
    ]
    assert r.codigo_eolica == 1
    r.codigo_eolica = 5
    assert r.data_inicial_estado_operacao == datetime(2021, 1, 1)
    r.data_inicial_estado_operacao = datetime(2021, 2, 1)
    assert r.data_final_estado_operacao == datetime(2030, 12, 1)
    r.data_final_estado_operacao = datetime(2030, 11, 1)
    assert r.estado_operacao == "centralizado"
    r.estado_operacao = "fixo"


def test_registro_pee_configuracao_periodo():
    m: MagicMock = mock_open(
        read_data="".join(MockRegistroPEEConfiguracaoPeriodo)
    )
    r = RegistroPEEConfiguracaoPeriodo()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [
        1,
        datetime(2021, 1, 1),
        datetime(2030, 12, 1),
        "centralizado",
    ]
    assert r.codigo_pee == 1
    r.codigo_pee = 5
    assert r.data_inicial_estado_operacao == datetime(2021, 1, 1)
    r.data_inicial_estado_operacao = datetime(2021, 2, 1)
    assert r.data_final_estado_operacao == datetime(2030, 12, 1)
    r.data_final_estado_operacao = datetime(2030, 11, 1)
    assert r.estado_operacao == "centralizado"
    r.estado_operacao = "fixo"


def test_registro_eolica_funcao_producao_eolicafte():
    m: MagicMock = mock_open(read_data="".join(MockRegistroFuncaoProducao))
    r = RegistroEolicaFTE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [
        1,
        datetime(2021, 1, 1),
        datetime(2030, 12, 1),
        -0.14454,
        0.109046,
    ]
    assert r.codigo_eolica == 1
    r.codigo_eolica = 5
    assert r.data_inicial == datetime(2021, 1, 1)
    r.data_inicial = datetime(2021, 2, 1)
    assert r.data_final == datetime(2030, 12, 1)
    r.data_final = datetime(2030, 11, 1)
    assert r.coeficiente_linear == -0.14454
    r.coeficiente_linear = -0.5
    assert r.coeficiente_angular == 0.109046
    r.coeficiente_angular = 0.5


def test_registro_peefte():
    m: MagicMock = mock_open(read_data="".join(MockRegistroPEEFTE))
    r = RegistroPEEFTE()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [
        1,
        datetime(2021, 1, 1),
        datetime(2030, 12, 1),
        -0.14454132687670500,
        0.10904637648150100,
    ]
    assert r.codigo_pee == 1
    r.codigo_pee = 5
    assert r.data_inicial == datetime(2021, 1, 1)
    r.data_inicial = datetime(2021, 2, 1)
    assert r.data_final == datetime(2030, 12, 1)
    r.data_final = datetime(2030, 11, 1)
    assert r.coeficiente_linear == -0.14454132687670500
    r.coeficiente_linear = -0.5
    assert r.coeficiente_angular == 0.10904637648150100
    r.coeficiente_angular = 0.5


def test_registro_eolica_geracao_patamar():
    m: MagicMock = mock_open(
        read_data="".join(MockRegistroEolicaGeracaoPatamar)
    )
    r = RegistroEolicaGeracaoPatamar()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, datetime(2021, 1, 1), datetime(2021, 1, 1), 2, 1.0496]
    assert r.codigo_eolica == 1
    r.codigo_eolica = 2
    assert r.data_inicial == datetime(2021, 1, 1)
    r.data_inicial = datetime(2022, 1, 1)
    assert r.data_final == datetime(2021, 1, 1)
    r.data_final = datetime(2022, 1, 1)
    assert r.indice_patamar == 2
    r.indice_patamar = 1
    assert r.profundidade == 1.0496
    r.profundidade = 2.0


def test_registro_pee_geracao_patamar():
    m: MagicMock = mock_open(read_data="".join(MockRegistroPEEGeracaoPatamar))
    r = RegistroPEEGeracaoPatamar()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, datetime(2021, 1, 1), datetime(2021, 1, 1), 1, 0.88]
    assert r.codigo_pee == 1
    r.codigo_pee = 2
    assert r.data_inicial == datetime(2021, 1, 1)
    r.data_inicial = datetime(2022, 1, 1)
    assert r.data_final == datetime(2021, 1, 1)
    r.data_final = datetime(2022, 1, 1)
    assert r.indice_patamar == 1
    r.indice_patamar = 2
    assert r.profundidade == 0.88
    r.profundidade = 2.0


def test_registro_eolica_historico_horizonte_eolicahistorico():
    m: MagicMock = mock_open(
        read_data="".join(MockRegistroEolicaHistoricoHorizonte)
    )
    r = RegistroEolicaHistoricoVentoHorizonte()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [datetime(1979, 1, 1), datetime(2016, 1, 1)]
    assert r.data_inicial == datetime(1979, 1, 1)
    r.data_inicial = datetime(1980, 1, 1)
    assert r.data_final == datetime(2016, 1, 1)
    r.data_final = datetime(2018, 1, 1)


def test_registro_eolica_historico_eolicahistorico():
    m: MagicMock = mock_open(read_data="".join(MockRegistroEolicaHistorico))
    r = RegistroEolicaHistoricoVento()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, datetime(1979, 1, 1), datetime(1979, 2, 1), 3.43, 1.0]
    assert r.codigo_eolica == 1
    r.codigo_eolica = 2
    assert r.data_inicial == datetime(1979, 1, 1)
    r.data_inicial = datetime(1980, 1, 1)
    assert r.data_final == datetime(1979, 2, 1)
    r.data_final = datetime(1980, 2, 1)
    assert r.velocidade == 3.43
    r.velocidade = 5.0
    assert r.direcao == 1.0
    r.direcao = 0.0


def test_registro_historico_vento_horizonte_eolicahistorico():
    m: MagicMock = mock_open(
        read_data="".join(MockRegistroHistoricoVentoHorizonte)
    )
    r = RegistroHistoricoVentoHorizonte()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [datetime(1979, 1, 1), datetime(2016, 1, 1)]
    assert r.data_inicial == datetime(1979, 1, 1)
    r.data_inicial = datetime(1980, 1, 1)
    assert r.data_final == datetime(2016, 1, 1)
    r.data_final = datetime(2018, 1, 1)


def test_registro_historico_vento_eolicahistorico():
    m: MagicMock = mock_open(read_data="".join(MockRegistroHistoricoVento))
    r = RegistroHistoricoVento()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, datetime(1979, 1, 1), datetime(1979, 2, 1), 4.05, 1.0]
    assert r.codigo_posto == 1
    r.codigo_posto = 2
    assert r.data_inicial == datetime(1979, 1, 1)
    r.data_inicial = datetime(1980, 1, 1)
    assert r.data_final == datetime(1979, 2, 1)
    r.data_final = datetime(1980, 2, 1)
    assert r.velocidade == 4.05
    r.velocidade = 5.0
    assert r.direcao == 1.0
    r.direcao = 0.0


def test_registro_posto_cadastro_eolicaposto():
    m: MagicMock = mock_open(read_data="".join(MockRegistroPostoCadastro))
    r = RegistroPostoVentoCadastro()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, "NEInterior"]
    assert r.codigo_posto == 1
    r.codigo_posto = 1
    assert r.nome_posto == "NEInterior"
    r.nome_posto = "NEInterior"


def test_registro_pee_posto_eolicaposto():
    m: MagicMock = mock_open(read_data="".join(MockRegistroPEEPosto))
    r = RegistroPEEPostoVento()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, 1]
    assert r.codigo_posto == 1
    r.codigo_posto = 2
    assert r.codigo_pee == 1
    r.codigo_pee = 2


def test_registro_eolica_submercado_eolicasubmercado():
    m: MagicMock = mock_open(read_data="".join(MockRegistroEolicaSubmercado))
    r = RegistroEolicaSubmercado()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [5, 2]
    assert r.codigo_eolica == 5
    r.codigo_eolica = 2
    assert r.codigo_submercado == 2
    r.codigo_submercado = 1


def test_registro_pee_submercado_eolicasubmercado():
    m: MagicMock = mock_open(read_data="".join(MockRegistroPEESubmercado))
    r = RegistroPEESubmercado()
    with patch("builtins.open", m):
        with open("", "") as fp:
            r.read(fp)

    assert r.data == [1, 3]
    assert r.codigo_pee == 1
    r.codigo_pee = 2
    assert r.codigo_submercado == 3
    r.codigo_submercado = 1


def test_atributos_encontrados():
    m: MagicMock = mock_open(read_data="".join(MockEolica))
    with patch("builtins.open", m):
        e = Eolica.read(ARQ_TESTE)
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
        assert len(e.eolica_configuracao()) > 0
        assert len(e.eolica_funcao_producao()) > 0
        assert len(e.eolica_geracao_profundidade_periodo_patamar()) > 0
        assert len(e.eolica_historico_vento()) > 0
        assert len(e.posto_vento_cad()) > 0
        assert len(e.pee_posto()) > 0
        assert len(e.eolica_submercado()) > 0


def test_eq_eolica():
    m: MagicMock = mock_open(read_data="".join(MockEolica))
    with patch("builtins.open", m):
        cf1 = Eolica.read(ARQ_TESTE)
        cf2 = Eolica.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_eolica():
    m: MagicMock = mock_open(read_data="".join(MockEolica))
    with patch("builtins.open", m):
        cf1 = Eolica.read(ARQ_TESTE)
        cf2 = Eolica.read(ARQ_TESTE)
        cf2.data.remove(cf1.eolica_cadastro()[0])
        assert cf1 != cf2


def test_leitura_escrita_eolica():
    m_leitura: MagicMock = mock_open(read_data="".join(MockEolica))
    with patch("builtins.open", m_leitura):
        cf1 = Eolica.read(ARQ_TESTE)
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
        cf2 = Eolica.read(ARQ_TESTE)
        assert cf1 == cf2
