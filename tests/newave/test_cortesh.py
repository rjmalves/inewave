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


def test_atributos_encontrados_cortesh():
    h = Cortesh.read(ARQ_TESTE)
    assert h.dados is not None


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
    assert h1.dados.versao_newave == 281200
    assert h1.dados.tamanho_corte == 17568
    assert h1.dados.tamanho_estado == 0
    assert h1.dados.numero_rees == 12
    assert h1.dados.numero_estagios_pre == 0
    assert h1.dados.numero_estagios_estudo == 60
    assert h1.dados.numero_estagios_pos == 60
    assert h1.dados.numero_estagios_ano == 12
    assert h1.dados.numero_configuracoes == 56
    assert h1.dados.numero_forwards == 200
    assert h1.dados.numero_patamares == 3
    assert h1.dados.ano_inicio_estudo == 2022
    assert h1.dados.mes_inicio_estudo == 5
    assert h1.dados.lag_maximo_gnl == 2
    assert h1.dados.mecanismo_aversao == 4
    assert h1.dados.numero_submercados == 4
    assert h1.dados.numero_total_submercados == 5
    assert h1.dados.usa_curva_aversao == 1
    assert h1.dados.usa_sar == 0
    assert h1.dados.usa_cvar == 1
    assert h1.dados.considera_no_zero_calculo_zinf == 0
    assert h1.dados.mes_agregacao == 17
    assert h1.dados.numero_maximo_uhes == 164
    assert h1.dados.considera_afluencia_anual == 0
    assert h1.dados.versao_nao_oficial == "CPAMP"
    assert h1.dados.tipo_penalizacao_curva == 1
    assert h1.dados.mes_penalizacao_curva == 11
    assert h1.dados.opcao_parpa == 3
    assert h1.dados.tipo_agregacao_caso == 0
    assert h1.dados.estagio_individualizado_inicial == 5
    assert h1.dados.estagio_individualizado_final == 16
    assert h1.dados.estagio_agregado_inicial == 17
    assert h1.dados.estagio_agregado_final == 120
    assert h1.dados.tamanho_registro_individualizado == 17568
    assert h1.dados.tamanho_registro_agregado == 1664
    assert h1.dados.ultimo_registro_cortes_estagio.shape == (120, 3)
    assert len(h1.dados.ordens_modelos_parp) == 1440
    assert len(h1.dados.configuracoes) == 120
    assert len(h1.dados.duracoes_patamares) == 180
    assert h1.dados.iteracao_atual == 30
    assert len(h1.dados.penalidade_violacao_curva) == 12
    assert len(h1.dados.curva_aversao) == 720
    assert h1.dados.flag_cvar == 1
    assert len(h1.dados.alfa_cvar) == 84
    assert len(h1.dados.lambda_cvar) == 84
    assert h1.dados.numero_uhes == 164
    assert len(h1.dados.codigos_uhes) == 164
    assert len(h1.dados.codigo_interno_ree_uhes) == 164
    assert len(h1.dados.rees_por_submercado) == 4
    assert len(h1.dados.codigos_internos_rees_por_submercado) == 12
    assert len(h1.dados.nomes_rees_submercados) == 16
    assert len(h1.dados.codigos_rees_submercados) == 16
    assert h1.dados.numero_coeficientes_derivacao_inexata_parpa == 7
    assert h1.dados.constante_numero_rees == 12
    assert h1.dados.constante_numero_rees_ordem_maxima_parp == 144
    assert (
        h1.dados.constante_numero_submercados_patamares_carga_lag_maximo_gnl
        == 24
    )
    assert h1.dados.constante_numero_maximo_uhes == 164
    assert h1.dados.constante_numero_maximo_uhes_ordem_maxima_parp == 1968
    assert len(h1.dados.numero_uhes_estagios_individualizados) == 17
    assert h1.dados.dados_uhes.shape == (164, 10)
    assert h1.dados.dados_submercados.shape == (5, 3)
