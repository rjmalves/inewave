from typing import Dict, List
import numpy as np  # type: ignore


class DadosGeraisPMO:
    """
    Armazena as informações de dados
    gerais contidas no arquivo `pmo.dat`.

    **Parâmetros**
    """
    def __init__(self):
        # TODO - estruturar as propriedades
        # Todas as informações echo do dger.dat.
        pass


class EnergiasAfluentesPMO:
    """
    Armazena as informações de energias
    afluentes anteriores ao estudo contidas no arquivo `pmo.dat`.

    **Parâmetros**
    """
    def __init__(self):
        # TODO - estruturar as propriedades
        pass


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


class PMO:
    """
    Armazena os dados de entrada do NEWAVE referentes ao
    acompanhamento do programa.

    Esta classe lida com as informações de entrada fornecidas ao
    NEWAVE e reproduzidas no `pmo.dat`, bem como as saídas finais
    da execução: custos de operação, energias, déficit, etc.

    Em versões futuras, esta classe pode passar a ler os dados
    de execução intermediárias do programa.

    **Parâmetros**

    - ano_pmo: `int`
    - mes_pmo: `int`
    - versao_newave: `str`
    - dados_gerais: `DadosGeraisPMO`
    - energias_passadas_politica: `EnergiasAfluentesPMO`
    - energias_passadas_primeira_conf: `EnergiasAfluentesPMO`
    - energias_passadas_canal_fuga: `EnergiasAfluentesPMO`
    - demanda_liquida_energia : `Dict[str, DemandaLiquidaEnergiaPMO]`
    - risco_ens: `RiscoDeficitENSPMO`
    - custo_series_simuladas: `CustoOperacaoPMO`
    - valor_esperado_periodo: `CustoOperacaoPMO`
    - custo_referenciado: `CustoOperacaoPMO`

    """
    def __init__(self,
                 ano_pmo: int,
                 mes_pmo: int,
                 versao_newave: str,
                 dados_gerais: DadosGeraisPMO,
                 energia_fio_liquida: EnergiaFioLiquidaREEPMO,
                 retas_perdas_engolimento: RetasPerdasEngolimentoREEPMO,
                 energias_passadas_politica: EnergiasAfluentesPMO,
                 energias_passadas_primeira_conf: EnergiasAfluentesPMO,
                 energias_passadas_canal_fuga: EnergiasAfluentesPMO,
                 demanda_liquida_energia: Dict[str,
                                               DemandaLiquidaEnergiaPMO],
                 risco_ens: RiscoDeficitENSPMO,
                 custo_series_simuladas: CustoOperacaoPMO,
                 valor_esperado_periodo: CustoOperacaoPMO,
                 custo_referenciado: CustoOperacaoPMO):
        self.ano_pmo = ano_pmo
        self.mes_pmo = mes_pmo
        self.versao_newave = versao_newave
        self.dados_gerais = dados_gerais
        self.energia_fio_liquida = energia_fio_liquida
        self.retas_perdas_engolimento = retas_perdas_engolimento
        self.energias_passadas_politica = energias_passadas_politica
        self.energias_passadas_primeira_conf = energias_passadas_primeira_conf
        self.energias_passadas_canal_fuga = energias_passadas_canal_fuga
        self.demanda_liquida_energia = demanda_liquida_energia
        self.risco_ens = risco_ens
        self.custo_series_simuladas = custo_series_simuladas
        self.valor_esperado_periodo = valor_esperado_periodo
        self.custo_referenciado = custo_referenciado
