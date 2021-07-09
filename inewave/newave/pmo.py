from inewave.config import REES
from inewave._utils.arquivo import Arquivo
from inewave._utils.bloco import Bloco
from inewave._utils.dadosarquivo import DadosArquivo
from inewave.newave.modelos.pmo import BlocoEcoDgerPMO
from inewave.newave.modelos.pmo import BlocoConvergenciaPMO
from inewave.newave.modelos.pmo import BlocoConfiguracoesExpansaoPMO
from inewave.newave.modelos.pmo import BlocoMARSPMO
from inewave.newave.modelos.pmo import BlocoRiscoDeficitENSPMO
from inewave.newave.modelos.pmo import BlocoCustoOperacaoPMO
from inewave.newave.modelos.pmo import LeituraPMO

from typing import Dict, List, Type
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class EnergiasAfluentesPMO:
    """
    Armazena as informações de energias
    afluentes anteriores ao estudo contidas no arquivo `pmo.dat`.

    **Parâmetros**
    """
    def __init__(self):
        # TODO - estruturar as propriedades
        pass

    def __eq__(self, o: object):
        return True


class EnergiaFioLiquidaREEPMO:
    """
    Armazena as informações de energias a fio d'água líquidas
    para cada REE existentes no arquivo `pmo.dat`,
    quando feita a simulação completa.

    **Parâmetros**

    - tabela: `np.ndarray`

    """

    def __init__(self,
                 tabela: np.ndarray):
        self.tabela = tabela

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre EnergiaFioLiquidaREEPMO avalia todos os campos.
        """
        if not isinstance(o, EnergiaFioLiquidaREEPMO):
            return False
        e: EnergiaFioLiquidaREEPMO = o
        return np.array_equal(self.tabela, e.tabela)


class ConfiguracoesExpansaoPMO:
    """
    Armazena as informações das configurações válidas para cada
    mês do estudo contidas no arquivo `pmo.dat`.

    **Parâmetros**

    - tabela: `np.ndarray`
    """
    def __init__(self,
                 tabela: np.ndarray):
        self.tabela = tabela

    def __eq__(self, o: object):
        """
        A igualdade entre ConfiguracoesExpansaoPMO avalia todos os campos.
        """
        if not isinstance(o, ConfiguracoesExpansaoPMO):
            return False
        e: ConfiguracoesExpansaoPMO = o
        return np.array_equal(self.tabela, e.tabela)

    @property
    def configs_por_ano(self) -> Dict[int, np.ndarray]:
        """
        Configurações ativas para serem consideradas em cada
        mês de estudo, organizada por ano.

        **Retorna**
        `Dict[int, np.ndarray]`
        """
        dict_configs: Dict[int, np.ndarray] = {}
        for lin in range(self.tabela.shape[0]):
            dict_configs[self.tabela[lin, 0]] = self.tabela[lin, 1:]

        return dict_configs


class RetasPerdasEngolimentoREEPMO:
    """
    Armazena as retas que modelam as perdas por engolimento
    máximo para cada REE, existentes no arquivo `pmo.dat`, quando
    feita a simulação completa.

    **Parâmetros**

    - tabela: `np.ndarray`

    """
    def __init__(self,
                 tabela: np.ndarray):
        self.tabela = tabela

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre RetasPerdasEngolimentoREEPMO
        avalia todos os campos.
        """
        if not isinstance(o, RetasPerdasEngolimentoREEPMO):
            return False
        e: RetasPerdasEngolimentoREEPMO = o
        return np.array_equal(self.tabela, e.tabela)

    def funcao_perdas(self,
                      ree: int,
                      energia_bruta: float) -> float:
        """
        Valor da função de perdas composta pelas retas
        para um determinado valor de energia bruta fornecido.

        **Parâmetros**

        - ree: `int`
        - energia_bruta: `float`

        **Retorna**
        `float`

        """
        n_lin = self.tabela.shape[0]
        # Calcula o valor das três retas na ordenada dada e
        # retorna o maior deles.
        energia = energia_bruta * np.ones((n_lin, 1))
        perdas: np.ndarray = np.multiply(self.tabela[ree-1, :, 1],
                                         energia) + self.tabela[ree-1, :, 2]
        return float(np.max(perdas))


class DemandaLiquidaEnergiaPMO:
    """
    Armazena as informações de demandas
    líquidas de energia contidas no arquivo `pmo.dat`.

    **Parâmetros**
    """
    def __init__(self):
        # TODO - estruturar as propriedades
        pass


class ConvergenciaPMO:
    """
    Armazena as informações do relatório de convergência do NEWAVE
    existentes no arquivo `pmo.dat`.

    **Parâmetros**

    - anos_estudo: `List[int]`
    - tabela: `np.ndarray`
    """
    def __init__(self,
                 tabela: np.ndarray):
        self.tabela = tabela

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre ConvergenciaPMO
        avalia todos os campos.
        """
        if not isinstance(o, ConvergenciaPMO):
            return False
        e: ConvergenciaPMO = o
        return np.array_equal(self.tabela, e.tabela)

    @property
    def zinf(self) -> Dict[int, List[float]]:
        """
        Limite inferior da função objetivo na PDDE (Zinf).

        **Retorna**

        `Dict[int, List[float]]`

        **Sobre**

        O número de chaves do dicionário é igual ao de iterações.
        """
        zinfs: Dict[int, List[float]] = {}
        for lin in range(self.tabela.shape[0]):
            it = int(self.tabela[lin, 0])
            if it not in zinfs:
                zinfs[it] = []
            zinfs[it].append(self.tabela[lin, 2])
        return zinfs

    @property
    def zsup(self) -> Dict[int, List[float]]:
        """
        Limite superior da função objetivo na PDDE (Zsup).

        **Retorna**

        `Dict[int, List[float]]`

        **Sobre**

        O número de chaves do dicionário é igual ao de iterações.
        """
        zsups: Dict[int, List[float]] = {}
        for lin in range(self.tabela.shape[0]):
            it = int(self.tabela[lin, 0])
            if it not in zsups:
                zsups[it] = []
            zsups[it].append(self.tabela[lin, 4])
        return zsups

    @property
    def tempos_execucao(self) -> List[float]:
        """
        Tempo de execução de cada iteração em segundos.

        **Retorna**

        `List[float]`

        **Sobre**

        O número de elementos da lista é igual ao de iterações.
        """
        tempos: List[float] = []
        ultima_it = -1
        for lin in range(self.tabela.shape[0]):
            it = self.tabela[lin, 0]
            if it == ultima_it:
                continue
            tempos.append(self.tabela[lin, -1])
            ultima_it = it
        return tempos


class RiscoDeficitENSPMO:
    """
    Armazena as informações risco de déficit e valores esperados
    de energia não supridacontidas no arquivo `pmo.dat`.

    **Parâmetros**

    - anos_estudo: `List[int]`
    - tabela: `np.ndarray`
    """
    def __init__(self,
                 anos_estudo: List[int],
                 tabela: np.ndarray):
        # São impressos no pmo.dat os subsistemas em
        # uma ordem pré-determinada
        self.subsistemas = ["SUDESTE",
                            "SUL",
                            "NORDESTE",
                            "NORTE"]
        self.anos_estudo = anos_estudo
        self.tabela = tabela

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre RiscoDeficitENSPMO
        avalia todos os campos.
        """
        if not isinstance(o, RiscoDeficitENSPMO):
            return False
        e: RiscoDeficitENSPMO = o
        eq_anos = all([a == b
                       for (a, b) in zip(self.anos_estudo,
                                         e.anos_estudo)])
        eq_tabela = np.array_equal(self.tabela, e.tabela)
        return eq_anos and eq_tabela

    @property
    def riscos_por_subsistema_e_ano(self) -> Dict[str,
                                                  Dict[int,
                                                       float]]:
        """
        Riscos de déficit agrupados por
        subsistema e ano de estudo.

        **Retorna**

        `Dict[str, Dict[int, float]]`

        **Sobre**

        O acesso é feito com
        [sub][ano] e o valor fornecido é em percentual, de 0 a 100.
        """
        riscos: Dict[str, Dict[int, float]] = {}
        for j, sub in enumerate(self.subsistemas):
            if sub not in riscos:
                riscos[sub] = {}
            for i, ano in enumerate(self.anos_estudo):
                riscos[sub][ano] = self.tabela[i, 2*j]
        return riscos

    @property
    def ens_por_subsistema_e_ano(self) -> Dict[str,
                                               Dict[int,
                                                    float]]:
        """
        Energias não supridas agrupadas por
        subsistema e ano de estudo.

        **Retorna**

        `Dict[str, Dict[int, float]]`

        **Sobre**

        O acesso é feito com
        [sub][ano] e o valor fornecido é em MWmes.
        """
        energias: Dict[str, Dict[int, float]] = {}
        for j, sub in enumerate(self.subsistemas):
            if sub not in energias:
                energias[sub] = {}
            for i, ano in enumerate(self.anos_estudo):
                energias[sub][ano] = self.tabela[i, 2*j + 1]
        return energias


class CustoOperacaoPMO:
    """
    Armazena as informações do relatório
    de custo de operação, disponível no arquivo `pmo.dat`.

    Esta classe armazena uma das tabelas existentes ao final do arquivo
    `pmo.dat`, contendo os custos, os desvios-padrão e a participação
    em percentual de cada componente de custo.

    A tabela de custos é armazenada através de uma array
    em `NumPy`, para otimizar cálculos futuros e espaço ocupado
    em memória. A tabela interna é transformada em dicionários
    e outras estruturas de dados mais palpáveis através das propriedades
    da própria classe.

    **Parâmetros**

    - custos: `np.ndarray`

    """
    def __init__(self,
                 custos: np.ndarray):
        self.custos = custos
        # TODO - fazer as @property de cada uma individualmente

        # self.geracao_termica = geracao_termica
        # self.deficit = deficit
        # self.vertimento = vertimento
        # self.excesso_energia = excesso_energia
        # self.violacao_car = violacao_car
        # self.violacao_sar = violacao_sar
        # self.violacao_outro_usos = violacao_outro_usos
        # self.violacao_evmin = violacao_evmin
        # self.violacao_vzmin = violacao_vzmin
        # self.intercambio = intercambio
        # self.violacao_intercambio_min = violacao_intercambio_min
        # self.vertimento_fio_nao_turbin = vertimento_fio_nao_turbin
        # self.violacao_ghmin = violacao_ghmin
        # self.violacao_ghmin_usina = violacao_ghmin_usina
        # self.violacao_retirada = violacao_retirada
        # self.violacao_emissao_gee = violacao_emissao_gee

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre CustoOperacaoPMO
        avalia todos os campos.
        """
        if not isinstance(o, CustoOperacaoPMO):
            return False
        e: CustoOperacaoPMO = o
        return np.array_equal(self.custos, e.custos)

    @property
    def geracao_termica(self) -> float:
        """
        Parcela do custo de operação devido à geração térmica,
        em MMR$.

        **Retorna**

        `float`
        """
        return float(self.custos[0, 0])

    @property
    def deficit(self) -> float:
        """
        Parcela do custo de operação devido ao déficit, em MMR$.

        **Retorna**

        `float`
        """
        return float(self.custos[1, 0])

    @property
    def custos_seguranca(self) -> float:
        """
        Parcela do custo de operação devido a violações de segurança,
        CAR e SAR, em MMR$.

        **Retorna**

        `float`
        """
        return np.sum(self.custos[4:6, 0])

    @property
    def custos_hidricos(self) -> float:
        """
        Parcela do custo de operação devido a violações de restrições
        hídricas, EVmin, VZmin, GHmin, GHmin Usina e outros usos
        da água, em MMR$.

        **Retorna**

        `float`
        """
        return (np.sum(self.custos[6:9, 0]) +
                np.sum(self.custos[12:14, 0]))

    @property
    def outros_custos(self) -> float:
        """
        Parcela do custo de operação devido a violações e penalidades
        de intercâmbio, intercâmbio mínimo, vertimento, vertimento
        fio d'água não turbinável, excesso de energia, emissão de GEE
        e retirada, em MMR$.

        **Retorna**

        `float`
        """
        return (np.sum(self.custos[2:4, 0]) +
                np.sum(self.custos[9:12, 0]) +
                np.sum(self.custos[14:, 0]))

    @property
    def custo_total(self) -> float:
        """
        Custo total de operação, em MMR$.

        **Retorna**

        `float`
        """
        return np.sum(self.custos[:, 0])


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

        `pandas.DataFrame`
        """
        df = pd.DataFrame(self.__convergencia[0].dados,
                          columns=[
                                   "Iteracao",
                                   "Lim. Inferior",
                                   "Zinf",
                                   "Lim. Superior",
                                   "Zsup",
                                   "Delta Zinf",
                                   "Zsup Iteracao",
                                   "Tempo (s)"
                                  ])
        # Constroi o DataFrame a partir da tabela do NumPy
        return df

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
