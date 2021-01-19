from typing import Dict, List
import numpy as np  # type: ignore


class DadosGeraisPMO:
    """
    Classe responsável por armazenar as informações de dados
    gerais contidas no arquivo pmo.dat.
    """
    def __init__(self):
        # TODO - estruturar as propriedades
        # Todas as informações echo do dger.dat.
        pass


class EnergiasAfluentesPMO:
    """
    Classe responsável por armazenar as informações de energias
    afluentes anteriores ao estudo contidas no arquivo pmo.dat.
    """
    def __init__(self):
        # TODO - estruturar as propriedades
        pass


class DemandaLiquidaEnergiaPMO:
    """
    Classe responsável por armazenar as informações de demandas
    líquidas de energia contidas no arquivo pmo.dat.
    """
    def __init__(self):
        # TODO - estruturar as propriedades
        pass


class RiscoDeficitENSPMO:
    """
    Classe responsável por armazenar as informações risco de déficit
    e valores esperados de energia não supridacontidas no arquivo pmo.dat.
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
        Representação dos riscos de déficit agrupados por
        subsistema e ano de estudo. O acesso é feito com
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
        Representação das energias não supridas agrupadas por
        subsistema e ano de estudo. O acesso é feito com
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
    Classe responsável por armazenar as informações do relatório
    de custo de operação, disponível no arquivo pmo.dat.
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
        """
        return float(self.custos[0, 0])

    @property
    def deficit(self) -> float:
        """
        Parcela do custo de operação devido ao déficit, em MMR$.
        """
        return float(self.custos[1, 0])

    @property
    def custos_seguranca(self) -> float:
        """
        Parcela do custo de operação devido a violações de segurança,
        CAR e SAR, em MMR$.
        """
        return np.sum(self.custos[4:6, 0])

    @property
    def custos_hidricos(self) -> float:
        """
        Parcela do custo de operação devido a violações de restrições
        hídricas, EVmin, VZmin, GHmin, GHmin Usina e outros usos
        da água, em MMR$.
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
        """
        return (np.sum(self.custos[2:4, 0]) +
                np.sum(self.custos[9:12, 0]) +
                np.sum(self.custos[14:, 0]))

    @property
    def custo_total(self) -> float:
        """
        Custo total de operação, em MMR$.
        """
        return np.sum(self.custos[:, 0])


class PMO:
    """
    Classe que armazena as informações estruturadas armazenadas no
    arquivo de saída do NEWAVE pmo.dat.
    """
    def __init__(self,
                 ano_pmo: int,
                 mes_pmo: int,
                 versao_newave: str,
                 dados_gerais: DadosGeraisPMO,
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
        self.energias_passadas_politica = energias_passadas_politica
        self.energias_passadas_primeira_conf = energias_passadas_primeira_conf
        self.energias_passadas_canal_fuga = energias_passadas_canal_fuga
        self.demanda_liquida_energia = demanda_liquida_energia
        self.risco_ens = risco_ens
        self.custo_series_simuladas = custo_series_simuladas
        self.valor_esperado_periodo = valor_esperado_periodo
        self.custo_referenciado = custo_referenciado