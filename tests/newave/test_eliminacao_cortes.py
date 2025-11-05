# Rotinas de testes associadas ao arquivo eliminacao_cortes.dat do NEWAVE
from unittest.mock import MagicMock, patch

from inewave.newave.modelos.eliminacao_cortes import BlocoParametrosEliminacaoCortes
from inewave.newave import EliminacaoCortes
from tests.mocks.arquivos.eliminacao_cortes import MockEliminacaoCortes
from tests.mocks.mock_open import mock_open

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_bloco_parametros_eliminacao_cortes():
    m: MagicMock = mock_open(read_data="".join(MockEliminacaoCortes))
    b = BlocoParametrosEliminacaoCortes()
    with patch("builtins.open", m):
        with open("", "") as fp:
            b.read(fp)

    assert len(b.data) == 7
    assert len(b.data[0]) == 3
    
    assert b.data[0][0] == 1 
    assert b.data[0][1] == 1  
    assert b.data[0][2] == 0
    
    assert b.data[4][0] == 5.00 


def test_atributos_nao_encontrados_eliminacao_cortes():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        ec = EliminacaoCortes.read(ARQ_TESTE)
        assert ec.algoritmo_avaliacao_paralelo is None
        assert ec.algoritmo_avaliacao_pares is None
        assert ec.algoritmo_avaliacao_shapiro is None
        assert ec.iteracao_inicial_paralelo is None
        assert ec.iteracao_inicial_pares is None
        assert ec.iteracao_inicial_shapiro is None
        assert ec.passo_aplicacao_paralelo is None
        assert ec.passo_aplicacao_pares is None
        assert ec.passo_aplicacao_shapiro is None
        assert ec.janela_iteracoes_pares is None
        assert ec.janela_iteracoes_shapiro is None
        assert ec.fator_limites_afluencias is None
        assert ec.afluencias_sim_final_calculo_limites is None
        assert ec.impressao_relatorios is None


def test_atributos_encontrados_eliminacao_cortes():
    m: MagicMock = mock_open(read_data="".join(MockEliminacaoCortes))
    with patch("builtins.open", m):
        ec = EliminacaoCortes.read(ARQ_TESTE)

        assert ec.algoritmo_avaliacao_paralelo == 1
        assert ec.algoritmo_avaliacao_pares == 1
        assert ec.algoritmo_avaliacao_shapiro == 0

        # Teste das iterações iniciais
        assert ec.iteracao_inicial_paralelo == 1
        assert ec.iteracao_inicial_pares == 1
        assert ec.iteracao_inicial_shapiro == 20

        # Teste dos passos de aplicação
        assert ec.passo_aplicacao_paralelo == 1
        assert ec.passo_aplicacao_pares == 1
        assert ec.passo_aplicacao_shapiro == 10

        # Teste das janelas de iterações
        assert ec.janela_iteracoes_pares == 50
        assert ec.janela_iteracoes_shapiro == 50

        # Teste do fator de afluências
        assert ec.fator_limites_afluencias == 5.00
        
        # Teste da configuração de afluências da simulação final
        assert ec.afluencias_sim_final_calculo_limites == 1
        
        # Teste da impressão de relatórios
        assert ec.impressao_relatorios == 0


def test_eq_eliminacao_cortes():
    m: MagicMock = mock_open(read_data="".join(MockEliminacaoCortes))
    with patch("builtins.open", m):
        ec1 = EliminacaoCortes.read(ARQ_TESTE)
        ec2 = EliminacaoCortes.read(ARQ_TESTE)
        assert ec1 == ec2


def test_neq_eliminacao_cortes():
    m1: MagicMock = mock_open(read_data="".join(MockEliminacaoCortes))
    m2: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m1):
        ec1 = EliminacaoCortes.read(ARQ_TESTE)
    with patch("builtins.open", m2):
        ec2 = EliminacaoCortes.read(ARQ_TESTE)
    assert ec1 != ec2


def test_leitura_escrita_eliminacao_cortes():
    m_leitura: MagicMock = mock_open(read_data="".join(MockEliminacaoCortes))
    with patch("builtins.open", m_leitura):
        ec1 = EliminacaoCortes.read(ARQ_TESTE)
    m_escrita: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m_escrita):
        ec1.write(ARQ_TESTE)
        # Recupera o que foi escrito
        chamadas = m_escrita.mock_calls
        linhas_escritas = [
            chamadas[i].args[0] for i in range(1, len(chamadas) - 1)
        ]
    m_releitura: MagicMock = mock_open(read_data="".join(linhas_escritas))
    with patch("builtins.open", m_releitura):
        ec2 = EliminacaoCortes.read(ARQ_TESTE)
        assert ec1 == ec2
