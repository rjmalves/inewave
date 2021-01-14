from typing import Dict
import numpy as np  # type: ignore


class MediasSIN:
    """
    Classe responsável por lidar com o armazenamento dos dados das
    saídas do NWListOP referentes às médias de diversas variáveis,
    existentes no arquivo MEDIAS-SIN.CSV.
    """
    def __init__(self,
                 mes_pmo: int,
                 tabela: np.ndarray):
        self.mes_pmo = mes_pmo
        self.tabela = tabela

    def extrai_variavel_tabela(self,
                               indice_variavel: int) -> np.ndarray:
        """
        Lógica para extrair uma variável qualquer da tabela de médias,
        partindo do índice dela (num. da linha).
        """
        return self.tabela[indice_variavel, :]

    @property
    def energias_armazenadas_absolutas(self) -> np.ndarray:
        """
        Retorna as energias armazenadas em valores absolutos (MWmed).
        A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(0)

    @property
    def energias_armazenadas_percentuais(self) -> np.ndarray:
        """
        Retorna as energias armazenadas em valores em percentual da EARMax.
        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(1)

    @property
    def percentil_10_energias_armazenadas(self) -> np.ndarray:
        """
        Retorna os valores para o percentil 10% da energia armazenada.
        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(2)

    @property
    def percentil_20_energias_armazenadas(self) -> np.ndarray:
        """
        Retorna os valores para o percentil 20% da energia armazenada.
        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(3)

    @property
    def percentil_30_energias_armazenadas(self) -> np.ndarray:
        """
        Retorna os valores para o percentil 30% da energia armazenada.
        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(4)

    @property
    def percentil_40_energias_armazenadas(self) -> np.ndarray:
        """
        Retorna os valores para o percentil 40% da energia armazenada.
        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(5)

    @property
    def percentil_50_energias_armazenadas(self) -> np.ndarray:
        """
        Retorna os valores para o percentil 50% da energia armazenada.
        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(6)

    @property
    def percentil_60_energias_armazenadas(self) -> np.ndarray:
        """
        Retorna os valores para o percentil 60% da energia armazenada.
        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(7)

    @property
    def percentil_70_energias_armazenadas(self) -> np.ndarray:
        """
        Retorna os valores para o percentil 70% da energia armazenada.
        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(8)

    @property
    def percentil_80_energias_armazenadas(self) -> np.ndarray:
        """
        Retorna os valores para o percentil 80% da energia armazenada.
        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(9)

    @property
    def percentil_90_energias_armazenadas(self) -> np.ndarray:
        """
        Retorna os valores para o percentil 90% da energia armazenada.
        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(10)

    @property
    def percentil_100_energias_armazenadas(self) -> np.ndarray:
        """
        Retorna os valores para o percentil 100% da energia armazenada.
        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(11)

    @property
    def energia_natural_afluente(self) -> np.ndarray:
        """
        Retorna as energias naturais afluentes em valores absolutos (MWmed).
        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(12)

    @property
    def energia_controlavel_corrigida(self) -> np.ndarray:
        """
        Retorna as energias controláveis corrigidas em valores absolutos
        (MWmed). A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(13)

    @property
    def energia_fio_dagua_bruta(self) -> np.ndarray:
        """
        Retorna as energias fio d'água brutas em valores absolutos
        (MWmed). A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(14)

    @property
    def energia_fio_dagua_liquida(self) -> np.ndarray:
        """
        Retorna as energias fio d'água líquidas em valores absolutos
        (MWmed). A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(15)

    @property
    def geracao_hidraulica_maxima(self) -> np.ndarray:
        """
        Retorna as gerações hidráulicas máximas em valores absolutos
        (MWmed). A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(16)

    @property
    def geracao_hidraulica_total(self) -> np.ndarray:
        """
        Retorna as gerações hidráulicas totais em valores absolutos
        (MWmed). A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(18)

    @property
    def geracao_hidraulica_controlavel(self) -> np.ndarray:
        """
        Retorna as gerações hidráulicas controláveis em valores absolutos
        (MWmed). A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(19)

    @property
    def geracao_hidraulica_fio_dagua_liquida(self) -> np.ndarray:
        """
        Retorna as gerações hidráulicas fio d'água líquidas em valores
        absolutos (MWmed). A série histórica
        retornada é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(20)

    @property
    def geracao_eolica(self) -> np.ndarray:
        """
        Retorna as gerações eólicas em valores absolutos (MWmed) para cada um
        dos submercados. A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(21)

    @property
    def geracao_solar(self) -> np.ndarray:
        """
        Retorna as gerações solares em valores absolutos (MWmed) para cada um
        dos submercados. A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(22)

    @property
    def vertimento_total(self) -> np.ndarray:
        """
        Retorna as perdas por vertimento totais em valores absolutos (MWmed).
        A série histórica retornada é dividida
        mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(23)

    @property
    def vertimento_controlavel(self) -> np.ndarray:
        """
        Retorna as perdas por vertimento controlável em valores absolutos
        (MWmed). A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(24)

    @property
    def vertimento_fio_dagua(self) -> np.ndarray:
        """
        Retorna as perdas por vertimento fio d'água em valores absolutos
        (MWmed). A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(25)

    @property
    def vertimento_turbinavel(self) -> np.ndarray:
        """
        Retorna os vertimentos turbináveis em valores absolutos
        (MWmed). A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(26)

    @property
    def energia_evaporada(self) -> np.ndarray:
        """
        Retorna as perdas por energia evaporada em valores absolutos
        (MWmed). A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(41)

    @property
    def geracao_termica(self) -> np.ndarray:
        """
        Retorna as gerações de usinas termelétricas em valores absolutos
        (MWmed). A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(43)

    @property
    def deficit(self) -> np.ndarray:
        """
        Retorna os déficits de carga em valores absolutos (MWmed).
        A série histórica retornada é dividida mensalmente,
        para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(44)

    @property
    def custo_termica(self) -> np.ndarray:
        """
        Retorna os custos de térmicas (MMR$). A série histórica retornada
        é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(45)

    @property
    def custo_deficit(self) -> np.ndarray:
        """
        Retorna os custos de déficit (MMR$). A série histórica retornada 
        é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(46)

    @property
    def custo_operacao_total(self) -> np.ndarray:
        """
        Retorna os custos de operação totais (MMR$). A série histórica
        retornada é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(47)

    @property
    def custo_operacao_mx(self) -> np.ndarray:
        """
        Retorna os custos de operação MX (MMR$). A série histórica
        retornada é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(48)

    @property
    def custo_operacao_violacao(self) -> np.ndarray:
        """
        Retorna os custos de operação por violação (MMR$). A série histórica
        retornada é dividida mensalmente, para todo o período de estudo.
        """
        return self.extrai_variavel_tabela(49)
