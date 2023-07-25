from inewave.newave.modelos.forwarh import SecaoDadosForwarh
from inewave.newave.forwarh import Forwarh

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch
import pytest

ARQ_TESTE = "./tests/mocks/arquivos/forwarh.dat"


def test_secao_dados_forwarh():
    r = SecaoDadosForwarh()
    with open(ARQ_TESTE, "rb") as fp:
        r.read(fp, storage="BINARY")

    assert len(r.data) == 128


def test_atributos_nao_encontrados_forwarh():
    m: MagicMock = mock_open(read_data=b"")
    with pytest.raises(ValueError):
        with patch("builtins.open", m):
            h = Forwarh.read(ARQ_TESTE)


def test_eq_forwarh():
    h1 = Forwarh.read(ARQ_TESTE)
    h2 = Forwarh.read(ARQ_TESTE)
    assert h1 == h2


def test_atributos_forwarh():
    h1 = Forwarh.read(ARQ_TESTE)
    assert (
        h1.nome_caso
        == "Backtest Preliminar CPAMP 2022-2023 - Hibrido NEWAVE 05/2021"
    )

    assert h1.numero_rees == 12
    assert h1.numero_submercados == 4
    assert h1.numero_total_submercados == 5
    assert h1.numero_series_gravadas == 2000
    assert h1.numero_aberturas == 20
    assert h1.numero_estagios_estudo == 60
    assert h1.intervalo_series_gravadas == 1
    assert h1.numero_classes_termicas_submercados == [34, 19, 43, 24]
    assert h1.numero_patamares_deficit == 1
    assert h1.tamanho_registro_arquivo_forward == 41264
    assert h1.numero_registros_arquivo_forward == 2000
    assert h1.numero_registros_necessarios_estagio == 1
    assert h1.ano_inicio_estudo == 2021
    assert h1.ano_inicio_historico_vazoes == 1
    assert h1.numero_anos_descontar_historico_vazoes == 0
    assert h1.numero_estagios_ano == 12
    assert h1.mes_inicio_estudo == 5
    assert h1.mes_inicio_pre_estudo == 1
    assert h1.numero_estagios_pre_estudo == 0
    assert h1.ordem_maxima_parp == 12
    assert h1.ano_inicio_series_historicas_simuladas == [0] * 100
    assert h1.numero_anos_historico_vazoes == 89
    assert h1.numero_patamares_carga == 3
    assert h1.simulacao_final_individualizada == 1
