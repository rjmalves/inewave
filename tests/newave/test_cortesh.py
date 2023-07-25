from inewave.newave.modelos.cortesh import SecaoDadosCortesh
from inewave.newave.cortesh import Cortesh

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch
import pytest

ARQ_TESTE = "./tests/mocks/arquivos/cortesh.dat"


def test_secao_dados_cortesh():
    r = SecaoDadosCortesh()
    with open(ARQ_TESTE, "rb") as fp:
        r.read(fp, storage="BINARY")

    assert len(r.data) == 23865
    assert r.versao_newave == 281200
    assert r.tamanho_corte == 17568
    assert r.tamanho_estado == 0
    assert r.numero_rees == 12
    assert r.numero_estagios_pre == 0
    assert r.numero_estagios_estudo == 60
    assert r.numero_estagios_pos == 60
    assert r.numero_estagios_ano == 12
    assert r.numero_configuracoes == 56
    assert r.numero_forwards == 200
    assert r.numero_patamares == 3
    assert r.ano_inicio_estudo == 2022
    assert r.mes_inicio_estudo == 5
    assert r.lag_maximo_gnl == 2
    assert r.mecanismo_aversao == 4
    assert r.numero_submercados == 4
    assert r.numero_total_submercados == 5
    assert r.usa_curva_aversao == 1
    assert r.usa_sar == 0
    assert r.usa_cvar == 1
    assert r.considera_no_zero_calculo_zinf == 0
    assert r.mes_agregacao == 17
    assert r.numero_maximo_uhes == 164
    assert r.considera_afluencia_anual == 0
    assert r.versao_nao_oficial == "CPAMP"
    assert r.tipo_penalizacao_curva == 1
    assert r.mes_penalizacao_curva == 11
    assert r.opcao_parpa == 3
    assert r.tipo_agregacao_caso == 0
    assert r.estagio_individualizado_inicial == 5
    assert r.estagio_individualizado_final == 16
    assert r.estagio_agregado_inicial == 17
    assert r.estagio_agregado_final == 120
    assert r.tamanho_registro_individualizado == 17568
    assert r.tamanho_registro_agregado == 1664
    assert r.ultimo_registro_cortes_estagio.shape == (120, 3)
    assert len(r.ordens_modelos_parp) == 1440
    assert len(r.configuracoes) == 120
    assert len(r.duracoes_patamares) == 180
    assert r.iteracao_atual == 30
    assert len(r.penalidade_violacao_curva) == 12
    assert len(r.curva_aversao) == 720
    assert r.flag_cvar == 1
    assert len(r.alfa_cvar) == 84
    assert len(r.lambda_cvar) == 84
    assert r.numero_uhes == 164
    assert len(r.codigos_uhes) == 164
    assert len(r.codigo_interno_ree_uhes) == 164
    assert len(r.rees_por_submercado) == 4
    assert len(r.codigos_internos_rees_por_submercado) == 12
    assert len(r.nomes_rees_submercados) == 16
    assert len(r.codigos_rees_submercados) == 16
    assert r.numero_coeficientes_derivacao_inexata_parpa == 7
    assert r.constante_numero_rees == 12
    assert r.constante_numero_rees_ordem_maxima_parp == 144
    assert r.constante_numero_submercados_patamares_carga_lag_maximo_gnl == 24
    assert r.constante_numero_maximo_uhes == 164
    assert r.constante_numero_maximo_uhes_ordem_maxima_parp == 1968
    assert len(r.numero_uhes_estagios_individualizados) == 17
    assert r.dados_uhes.shape == (164, 10)
    assert r.dados_submercados.shape == (5, 3)


def test_atributos_encontrados_cortesh():
    h = Cortesh.read(ARQ_TESTE)
    assert h.versao_newave is not None


def test_atributos_nao_encontrados_cortesh():
    m: MagicMock = mock_open(read_data=b"")
    with pytest.raises(ValueError):
        with patch("builtins.open", m):
            h = Cortesh.read(ARQ_TESTE)


def test_eq_cortesh():
    h1 = Cortesh.read(ARQ_TESTE)
    h2 = Cortesh.read(ARQ_TESTE)
    assert h1 == h2


def test_atributos_cortesh():
    h1 = Cortesh.read(ARQ_TESTE)
    assert h1.versao_newave == 281200
    assert h1.tamanho_corte == 17568
    assert h1.tamanho_estado == 0
    assert h1.numero_rees == 12
    assert h1.numero_estagios_pre == 0
    assert h1.numero_estagios_estudo == 60
    assert h1.numero_estagios_pos == 60
    assert h1.numero_estagios_ano == 12
    assert h1.numero_configuracoes == 56
    assert h1.numero_forwards == 200
    assert h1.numero_patamares == 3
    assert h1.ano_inicio_estudo == 2022
    assert h1.mes_inicio_estudo == 5
    assert h1.lag_maximo_gnl == 2
    assert h1.numero_submercados == 4
    assert h1.numero_total_submercados == 5
    assert h1.mes_agregacao == 17
    assert h1.numero_maximo_uhes == 164
    assert h1.considera_afluencia_anual == 0
    assert h1.tipo_agregacao_caso == 0
    assert h1.estagio_individualizado_inicial == 5
    assert h1.estagio_individualizado_final == 16
    assert h1.estagio_agregado_inicial == 17
    assert h1.estagio_agregado_final == 120
    assert h1.tamanho_registro_individualizado == 17568
    assert h1.tamanho_registro_agregado == 1664
    assert h1.ultimo_registro_cortes_estagio.shape == (120, 3)
    assert h1.dados_uhes.shape == (164, 10)
    assert h1.dados_submercados.shape == (5, 3)
