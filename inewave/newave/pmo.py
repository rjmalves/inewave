from inewave.config import REES
from inewave._utils.arquivo import Arquivo
from inewave._utils.bloco import Bloco
from inewave._utils.dadosarquivo import DadosArquivo
from inewave.newave.modelos.pmo import BlocoEcoDgerPMO
from inewave.newave.modelos.pmo import BlocoEafPastTendenciaHidrolPMO
from inewave.newave.modelos.pmo import BlocoEafPastCfugaMedioPMO
from inewave.newave.modelos.pmo import BlocoConvergenciaPMO
from inewave.newave.modelos.pmo import BlocoConfiguracoesExpansaoPMO
from inewave.newave.modelos.pmo import BlocoMARSPMO
from inewave.newave.modelos.pmo import BlocoRiscoDeficitENSPMO
from inewave.newave.modelos.pmo import BlocoCustoOperacaoPMO
from inewave.newave.modelos.pmo import LeituraPMO

from typing import Dict, List, Type
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class PMO(Arquivo):
    """
    Armazena os dados de entrada do NEWAVE referentes ao
    acompanhamento do programa.

    Esta classe lida com as informações de entrada fornecidas ao
    NEWAVE e reproduzidas no `pmo.dat`, bem como as saídas finais
    da execução: custos de operação, energias, déficit, etc.

    Em versões futuras, esta classe pode passar a ler os dados
    de execução intermediárias do programa.

    """
    def __init__(self,
                 dados: DadosArquivo):
        super().__init__(dados)

        self.__eco_dger = self.__por_tipo(BlocoEcoDgerPMO)
        self.__eafpast_th = self.__por_tipo(BlocoEafPastTendenciaHidrolPMO)
        self.__eafpast_cfuga = self.__por_tipo(BlocoEafPastCfugaMedioPMO)
        self.__convergencia = self.__por_tipo(BlocoConvergenciaPMO)
        self.__configs_exp = self.__por_tipo(BlocoConfiguracoesExpansaoPMO)
        self.__mars = self.__por_tipo(BlocoMARSPMO)
        self.__risco_deficit = self.__por_tipo(BlocoRiscoDeficitENSPMO)
        self.__custos = self.__por_tipo(BlocoCustoOperacaoPMO)

    def __por_tipo(self, tipo: Type[Bloco]) -> List[Bloco]:
        return [b for b in self._blocos if isinstance(b, tipo)]

    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="pmo.dat") -> 'PMO':
        leitor = LeituraPMO(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    @property
    def eafpast_tendencia_hidrologica(self) -> pd.DataFrame:
        """
        Energias afluentes passadas por REE para análise da tendência
        hidrológica, em relação à primeira configuração do sistema,
        em MWmes.

        **Retorna**

        `pd.DataFrame`
        """
        return self.__eafpast_th[0].dados

    @eafpast_tendencia_hidrologica.setter
    def eafpast_tendencia_hidrologica(self, eaf: pd.DataFrame):
        self.__eafpast_th[0].dados = eaf

    @property
    def eafpast_cfuga_medio(self) -> pd.DataFrame:
        """
        Energias afluentes passadas por REE considerando canal de
        fuga médio, em relação à primeira configuração do sistema,
        em MWmes.

        **Retorna**

        `pd.DataFrame`
        """
        return self.__eafpast_cfuga[0].dados

    @eafpast_cfuga_medio.setter
    def eafpast_cfuga_medio(self, eaf: pd.DataFrame):
        self.__eafpast_cfuga[0].dados = eaf

    @property
    def configuracoes_entrada_reservatorio(self) -> np.ndarray:
        """
        Configurações do sistema em cada período devido a entrada
        de reservatórios e/ou potência de base.

        **Retorna**

        `np.ndarray`
        """
        return self.__configs_exp[0].dados

    @configuracoes_entrada_reservatorio.setter
    def configuracoes_entrada_reservatorio(self, configs: np.ndarray):
        self.__configs_exp[0].dados = configs

    @property
    def configuracoes_alteracao_potencia(self) -> np.ndarray:
        """
        Configurações do sistema em cada período devido a alterações
        de potência.

        **Retorna**

        `np.ndarray`
        """
        return self.__configs_exp[1].dados

    @configuracoes_alteracao_potencia.setter
    def configuracoes_alteracao_potencia(self, configs: np.ndarray):
        self.__configs_exp[1].dados = configs

    @property
    def configuracoes_qualquer_modificacao(self) -> np.ndarray:
        """
        Configurações do sistema em cada período devido a alterações
        de potência.

        **Retorna**

        `np.ndarray`
        """
        return self.__configs_exp[2].dados

    @configuracoes_qualquer_modificacao.setter
    def configuracoes_qualquer_modificacao(self, configs: np.ndarray):
        self.__configs_exp[2].dados = configs

    @property
    def retas_perdas_engolimento(self) -> Dict[str, np.ndarray]:
        """
        Retas ajustadas segundo o modelo MARS para corrigir a
        energia fio d'água com as perdas por engolimento máximo.

        OBS:
        Retorna apenas o modelo ajustado para a configuração do
        primeiro período de estudo (temporariamente).

        **Retorna**

        `np.ndarray`
        """
        retas: Dict[str, np.ndarray] = {}
        for i, r in enumerate(REES):
            retas[r] = self.__mars[0].dados[:, :, i]
        return retas

    @property
    def convergencia(self) -> pd.DataFrame:
        """
        Tabela de convergência da execução do NEWAVE.

        **Retorna**

        `pd.DataFrame`
        """
        return self.__convergencia[0].dados

    @property
    def risco_deficit_ens(self) -> pd.DataFrame:
        """
        Tabela de riscos de déficit e enegia não suprida (ENS).

        **Retorna**

        `pandas.DataFrame`
        """
        df = pd.DataFrame(self.__risco_deficit[0].dados,
                          columns=[
                                   "Ano",
                                   "Risco (%) SE",
                                   "EENS (MWMes) SE",
                                   "Risco (%) S",
                                   "EENS (MWMes) S",
                                   "Risco (%) NE",
                                   "EENS (MWMes) NE",
                                   "Risco (%) N",
                                   "EENS (MWMes) N"
                                  ])
        return df

    @property
    def custo_operacao_series_simuladas(self) -> pd.DataFrame:
        """
        Tabela de custos de operação categorizados para as
        séries simuladas.

        **Retorna**

        `pandas.DataFrame`
        """
        df = pd.DataFrame(self.__custos[0].dados,
                          columns=[
                                   "Valor Esperado",
                                   "Desvio Padrão do VE",
                                   "(%)"
                                  ])
        indices = pd.Series(BlocoCustoOperacaoPMO.componentes_custo)
        df.set_index(indices,
                     inplace=True)
        return df

    @property
    def valor_esperado_periodo_estudo(self) -> pd.DataFrame:
        """
        Tabela de custos de operação esperados para o período
        de estudo.

        **Retorna**

        `pandas.DataFrame`
        """
        df = pd.DataFrame(self.__custos[1].dados,
                          columns=[
                                   "Valor Esperado",
                                   "Desvio Padrão do VE",
                                   "(%)"
                                  ])
        indices = pd.Series(BlocoCustoOperacaoPMO.componentes_custo)
        df.set_index(indices,
                     inplace=True)
        return df

    @property
    def custo_operacao_referenciado_primeiro_mes(self) -> pd.DataFrame:
        """
        Tabela de custos de operação esperados para o período
        de estudo, referenciados ao primeiro mês.

        **Retorna**

        `pandas.DataFrame`
        """
        df = pd.DataFrame(self.__custos[2].dados,
                          columns=[
                                   "Valor Esperado",
                                   "Desvio Padrão do VE",
                                   "(%)"
                                  ])
        indices = pd.Series(BlocoCustoOperacaoPMO.componentes_custo)
        df.set_index(indices,
                     inplace=True)
        return df
