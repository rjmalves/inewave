# Imports do próprio módulo
from inewave._utils.leitura import Leitura
from .modelos.dger import DGer, EnumTipoExecucao
# Imports de módulos externos
import os
from traceback import print_exc


class LeituraDGer(Leitura):
    """
    Classe para realizar a leitura do arquivo dger.dat
    existente em um diretório de entradas do NEWAVE.
    """
    def __init__(self,
                 diretorio: str) -> None:
        super().__init__()
        self.diretorio = diretorio
        # DGer default, depois é substituído
        self.dger = DGer.dger_padrao()

    def le_arquivo(self) -> DGer:
        try:
            caminho = os.path.join(self.diretorio, "dger.dat")
            with open(caminho, "r") as arq:
                # Lê o nome do estudo e restringe até a coluna 80
                nome = self._le_linha_com_backup(arq)
                self.dger.nome_estudo = nome[:min([79, len(nome)])]
                # Lê os demais parâmetros
                ci = 21
                cf = 25

                def le_parametro():
                    return self._le_linha_com_backup(arq)[ci:cf].strip()

                # Tipo de execução
                p = le_parametro()
                tipo_exec = (EnumTipoExecucao.COMPLETA if p == "1"
                             else EnumTipoExecucao.SIMULACAO_FINAL)
                self.dger.tipo_execucao = tipo_exec
                # Duração do período
                self.dger.duracao_estagio_op = int(le_parametro())
                # Num. anos do estudo
                self.dger.num_anos_estudo = int(le_parametro())
                # Mês início do pré-estudo
                self.dger.mes_inicio_pre_estudo = int(le_parametro())
                # Mês início do estudo
                self.dger.mes_inicio_estudo = int(le_parametro())
                # Ano de início do estudo
                self.dger.ano_inicio_estudo = int(le_parametro())
                # Num. anos pré-estudo
                self.dger.num_anos_pre_estudo = int(le_parametro())
                # Num. anos pós estudo
                self.dger.num_anos_pos_estudo = int(le_parametro())
                # Num. anos pós estudo na sim final
                self.dger.num_anos_pos_sim_final = int(le_parametro())
                # Impressão de dados das usinas
                p = le_parametro()
                self.dger.imprime_dados_usinas = (True if p == "1"
                                                  else False)
                # Impressão de dados dos mercados
                p = le_parametro()
                self.dger.imprime_dados_mercados = (True if p == "1"
                                                    else False)
                # Impressão de dados de energias
                p = le_parametro()
                self.dger.imprime_dados_energias = (True if p == "1"
                                                    else False)
                # Impressão de dados do modelo estocástico
                p = le_parametro()
                self.dger.imprime_dados_modelo = (True if p == "1"
                                                  else False)
                # Impressão de dados das REEs
                p = le_parametro()
                self.dger.imprime_dados_rees = (True if p == "1"
                                                else False)
                # Máximo de iterações
                self.dger.max_iteracoes = int(le_parametro())
                # Num. de forwards
                self.dger.num_sim_forward = int(le_parametro())
                # Num. de aberturas
                self.dger.num_aberturas = int(le_parametro())
                # Num. de séries sintéticas
                self.dger.num_series_sinteticas = int(le_parametro())
                # Ordem máxima do Par(P)
                self.dger.ordem_maxima_parp = int(le_parametro())
                # Ano inicial do histórico de afluências e tamanho
                p = self._le_linha_com_backup(arq)
                self.dger.ano_inicial_vaz_historicas = int(p[ci:cf].strip())
                self.dger.tamanho_arq_vaz_historicas = int(p[28])
                # Cálculo da energia armazenada dos volumes iniciais
                p = le_parametro()
                self.dger.calcula_vol_inicial = (True if p == "1"
                                                 else False)
                # Ignora a linha de cabeçalho dos volumes iniciais
                self._le_linha_com_backup(arq)
                # Lê os volumes de cada subsistema
                p = self._le_linha_com_backup(arq)
                cisub = 22
                n_col_sub = 5
                for i in range(4):
                    cfsub = cisub + n_col_sub
                    v = float(p[cisub:cfsub])
                    self.dger.vol_inicial_subsistema[i] = v
                    cisub = cfsub + 2
                # TODO - continuar a partir da tolerância
                return self.dger
        except Exception:
            print_exc()
            return self.dger

    def _fim_arquivo(self, linha: str) -> bool:
        return False
