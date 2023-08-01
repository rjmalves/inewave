# Rotinas de testes associadas ao arquivo eolica-config.csv do NEWAVE
from datetime import datetime
from inewave.newave.modelos.eolicaconfiguracao import (
    RegistroEolicaConfiguracao,
    RegistroPEEConfiguracaoPeriodo,
)

from inewave.newave.eolicaconfiguracao import EolicaConfiguracao

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.eolicaconfig import (
    MockRegistroEolicaConfiguracaoPeriodo,
    MockRegistroPEEConfiguracaoPeriodo,
    MockEolicaConfig,
)

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_registro_eolica_configuracao_periodo_eolicaconfig():
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


def test_registro_pee_configuracao_periodo_eolicaconfig():
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


def test_atributos_encontrados_eolicaconfig():
    m: MagicMock = mock_open(read_data="".join(MockEolicaConfig))
    with patch("builtins.open", m):
        e = EolicaConfiguracao.read(ARQ_TESTE)
        assert len(e.eolica_configuracao()) > 0


def test_eq_eolicaconfig():
    m: MagicMock = mock_open(read_data="".join(MockEolicaConfig))
    with patch("builtins.open", m):
        cf1 = EolicaConfiguracao.read(ARQ_TESTE)
        cf2 = EolicaConfiguracao.read(ARQ_TESTE)
        assert cf1 == cf2


def test_neq_eolicaconfig():
    m: MagicMock = mock_open(read_data="".join(MockEolicaConfig))
    with patch("builtins.open", m):
        cf1 = EolicaConfiguracao.read(ARQ_TESTE)
        cf2 = EolicaConfiguracao.read(ARQ_TESTE)
        cf2.data.remove(cf1.eolica_configuracao()[0])
        assert cf1 != cf2


def test_leitura_escrita_eolicaconfig():
    m_leitura: MagicMock = mock_open(read_data="".join(MockEolicaConfig))
    with patch("builtins.open", m_leitura):
        cf1 = EolicaConfiguracao.read(ARQ_TESTE)
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
        cf2 = EolicaConfiguracao.read(ARQ_TESTE)
        assert cf1 == cf2
