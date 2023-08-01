from inewave.newave.modelos.pmo import BlocoEafPastTendenciaHidrolPMO
from inewave.newave.modelos.pmo import BlocoEafPastCfugaMedioPMO
from inewave.newave.modelos.pmo import BlocoConvergenciaPMO
from inewave.newave.modelos.pmo import BlocoConfiguracoesExpansaoPMO
from inewave.newave.modelos.pmo import BlocoMARSPMO
from inewave.newave.modelos.pmo import BlocoRiscoDeficitENSPMO
from inewave.newave.modelos.pmo import BlocoCustoOperacaoPMO
from inewave.newave.modelos.pmo import BlocoCustoOperacaoTotalPMO
from inewave.newave.modelos.pmo import BlocoProdutibilidadesConfiguracaoPMO

from cfinterface.files.blockfile import BlockFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Pmo(BlockFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao
    acompanhamento do programa.

    Esta classe lida com as informações de entrada fornecidas ao
    NEWAVE e reproduzidas no `pmo.dat`, bem como as saídas finais
    da execução: custos de operação, energias, déficit, etc.

    Em versões futuras, esta classe pode passar a ler os dados
    de execução intermediárias do programa.

    """

    T = TypeVar("T")

    BLOCKS = [
        BlocoEafPastTendenciaHidrolPMO,
        BlocoEafPastCfugaMedioPMO,
        BlocoConvergenciaPMO,
        BlocoConfiguracoesExpansaoPMO,
        BlocoMARSPMO,
        BlocoRiscoDeficitENSPMO,
        BlocoCustoOperacaoPMO,
        BlocoCustoOperacaoTotalPMO,
        BlocoProdutibilidadesConfiguracaoPMO,
    ]

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="pmo.dat") -> "Pmo":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    @property
    def eafpast_tendencia_hidrologica(self) -> Optional[pd.DataFrame]:
        """
        Energias afluentes passadas por REE para análise da tendência
        hidrológica, em relação à primeira configuração do sistema,
        em MWmes.

        - ree (`str`)
        - janeiro (`float`)
        - fevereiro (`float`)
        - ...
        - dezembro (`float`)

        :return: A tendência hidrológica em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoEafPastTendenciaHidrolPMO)
        if isinstance(b, BlocoEafPastTendenciaHidrolPMO):
            return b.data
        return None

    @property
    def eafpast_cfuga_medio(self) -> Optional[pd.DataFrame]:
        """
        Energias afluentes passadas por REE considerando canal de
        fuga médio, em relação à primeira configuração do sistema,
        em MWmes.

        - ree (`str`)
        - janeiro (`float`)
        - fevereiro (`float`)
        - ...
        - dezembro (`float`)

        :return: As energias afluentes passadas.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoEafPastCfugaMedioPMO)
        if isinstance(b, BlocoEafPastCfugaMedioPMO):
            return b.data
        return None

    @property
    def configuracoes_entrada_reservatorio(self) -> Optional[pd.DataFrame]:
        """
        Configurações do sistema em cada período devido a entrada
        de reservatórios e/ou potência de base.

        - ano (`int`)
        - janeiro (`float`)
        - fevereiro (`float`)
        - ...
        - dezembro (`float`)

        :return: As configurações em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoConfiguracoesExpansaoPMO)
        if isinstance(b, list):
            return b[0].data
        return None

    @property
    def configuracoes_alteracao_potencia(self) -> Optional[pd.DataFrame]:
        """
        Configurações do sistema em cada período devido a alterações
        de potência.

        - ano (`int`)
        - janeiro (`float`)
        - fevereiro (`float`)
        - ...
        - dezembro (`float`)

        :return: As configurações em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoConfiguracoesExpansaoPMO)
        if isinstance(b, list):
            return b[1].data
        return None

    @property
    def configuracoes_qualquer_modificacao(self) -> Optional[pd.DataFrame]:
        """
        Configurações do sistema em cada período devido a alterações
        de potência.

        - ano (`int`)
        - janeiro (`float`)
        - fevereiro (`float`)
        - ...
        - dezembro (`float`)

        :return: As configurações em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoConfiguracoesExpansaoPMO)
        if isinstance(b, list):
            return b[2].data
        return None

    def retas_perdas_engolimento(self, estagio: int) -> Optional[pd.DataFrame]:
        """
        Retas ajustadas segundo o modelo MARS para corrigir a
        energia fio d'água com as perdas por engolimento máximo.

        - ree (`str`)
        - reta (`int`)
        - coeficiente_angular (`float`)
        - coeficiente_linear (`float`)

        :return: As retas em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoMARSPMO)
        if isinstance(b, list):
            return b[estagio - 1].data
        return None

    @property
    def convergencia(self) -> Optional[pd.DataFrame]:
        """
        Tabela de convergência da execução do NEWAVE.

        - iteracao (`int`)
        - limite_inferior_zinf (`float`)
        - zinf (`float`)
        - limite_superior_zinf (`float`)
        - zsup (`float`)
        - delta_zinf (`float`)
        - zsup_iteracao (`float`)
        - tempo (`timedelta`)

        :return: As convergência em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoConvergenciaPMO)
        if isinstance(b, BlocoConvergenciaPMO):
            return b.data
        return None

    @property
    def risco_deficit_ens(self) -> Optional[pd.DataFrame]:
        """
        Tabela de riscos de déficit e enegia não suprida (ENS).

        - ano (`int`)
        - risco_<nome_submercado_1> (`float`)
        - eens_<nome_submercado_1> (`float`)
        - ...
        - risco_<nome_submercado_N> (`float`)
        - eens_<nome_submercado_N> (`float`)

        :return: Os ricos em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoRiscoDeficitENSPMO)
        if isinstance(b, BlocoRiscoDeficitENSPMO):
            return b.data
        return None

    @property
    def custo_operacao_series_simuladas(self) -> Optional[pd.DataFrame]:
        """
        Tabela de custos de operação categorizados para as
        séries simuladas.

        - parcela (`str`)
        - valor_esperado (`float`)
        - desvio_padrao (`float`)
        - percentual (`float`)

        :return: Os custos em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoCustoOperacaoPMO)
        if isinstance(b, list):
            return b[0].data
        return None

    @property
    def valor_esperado_periodo_estudo(self) -> Optional[pd.DataFrame]:
        """
        Tabela de custos de operação esperados para o período
        de estudo.

        - parcela (`str`)
        - valor_esperado (`float`)
        - desvio_padrao (`float`)
        - percentual (`float`)

        :return: Os custos em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoCustoOperacaoPMO)
        if isinstance(b, list):
            return b[1].data
        return None

    @property
    def custo_operacao_referenciado_primeiro_mes(
        self,
    ) -> Optional[pd.DataFrame]:
        """
        Tabela de custos de operação esperados para o período
        de estudo, referenciados ao primeiro mês.

        - parcela (`str`)
        - valor_esperado (`float`)
        - desvio_padrao (`float`)
        - percentual (`float`)

        :return: Os custos em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoCustoOperacaoPMO)
        if isinstance(b, list):
            return b[2].data
        return None

    @property
    def custo_operacao_total(self) -> Optional[float]:
        """
        Custo de operacao total da SF.

        :return: O custo total.
        :rtype: float | None
        """
        b = self.data.get_blocks_of_type(BlocoCustoOperacaoTotalPMO)
        if isinstance(b, BlocoCustoOperacaoTotalPMO):
            return b.data[0]
        return None

    @property
    def desvio_custo_operacao_total(self) -> Optional[float]:
        """
        O desvio padrão do custo de operacao total da SF.

        :return: O desvio do custo total.
        :rtype: float | None
        """
        b = self.data.get_blocks_of_type(BlocoCustoOperacaoTotalPMO)
        if isinstance(b, BlocoCustoOperacaoTotalPMO):
            return b.data[1]
        return None

    @property
    def produtibilidades_equivalentes(self) -> Optional[pd.DataFrame]:
        """
        Tabela de produtibilidades calculadas para diversos fins do NEWAVE
        por usina e por configuração.

        - nome_usina (`str`)
        - configuracao (`int`)
        - produtibilidade_equivalente_volmin_volmax (`float`)
        - produtibilidade_equivalente_volmin_vol65 (`float`)
        - produtibilidade_altura_minima (`float`)
        - produtibilidade_altura_65 (`float`)
        - produtibilidade_altura_maxima (`float`)
        - produtibilidade_acumulada_calculo_earm (`float`)
        - produtibilidade_acumulada_calculo_earm_65 (`float`)
        - produtibilidade_acumulada_calculo_econ (`float`)
        - produtibilidade_acumulada_calculo_altura_minima (`float`)
        - produtibilidade_acumulada_calculo_altura_65 (`float`)
        - produtibilidade_acumulada_calculo_altura_maxima (`float`)
        - produtibilidade_acumulada_calculo_evaporacao_altura_minima (`float`)
        - produtibilidade_acumulada_calculo_evaporacao_altura_65 (`float`)
        - produtibilidade_acumulada_calculo_evaporacao_altura_maxima (`float`)


        :return: As produtibilidades em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoProdutibilidadesConfiguracaoPMO)
        if isinstance(b, BlocoProdutibilidadesConfiguracaoPMO):
            return b.data
        return None
