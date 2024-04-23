from inewave.newave.modelos.pmo import BlocoVersaoModeloPMO
from inewave.newave.modelos.pmo import BlocoEafPastTendenciaHidrolPMO
from inewave.newave.modelos.pmo import BlocoEafPastCfugaMedioPMO
from inewave.newave.modelos.pmo import BlocoConvergenciaPMO
from inewave.newave.modelos.pmo import BlocoConfiguracoesExpansaoPMO
from inewave.newave.modelos.pmo import BlocoMARSPMO
from inewave.newave.modelos.pmo import BlocoRiscoDeficitENSPMO
from inewave.newave.modelos.pmo import BlocoCustoOperacaoPMO
from inewave.newave.modelos.pmo import BlocoCustoOperacaoTotalPMO
from inewave.newave.modelos.pmo import BlocoProdutibilidadesConfiguracaoPMO
from inewave.newave.modelos.pmo import BlocoEnergiaArmazenadaMaximaPMO
from inewave.newave.modelos.pmo import BlocoEnergiaArmazenadaInicialPMO
from inewave.newave.modelos.pmo import BlocoVolumeArmazenadoInicialPMO
from inewave.newave.modelos.pmo import BlocoPenalidadeViolacaoOutrosUsosPMO
from inewave.newave.modelos.pmo import BlocoPenalidadeViolacaoVazaoMinimaPMO
from inewave.newave.modelos.pmo import BlocoPenalidadeViolacaoCurvaSegurancaPMO
from inewave.newave.modelos.pmo import BlocoPenalidadeViolacaoFphaPMO
from inewave.newave.modelos.pmo import BlocoPenalidadeViolacaoEvaporacaoPMO
from inewave.newave.modelos.pmo import (
    BlocoPenalidadeViolacaoTurbinamentoMaximoPMO,
)
from inewave.newave.modelos.pmo import (
    BlocoPenalidadeViolacaoTurbinamentoMinimoPMO,
)
from inewave.newave.modelos.pmo import (
    BlocoGeracaoMinimaUsinasTermicasPMO,
    BlocoGeracaoMaximaUsinasTermicasPMO,
)

from cfinterface.files.blockfile import BlockFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


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
        BlocoVersaoModeloPMO,
        BlocoEafPastTendenciaHidrolPMO,
        BlocoEafPastCfugaMedioPMO,
        BlocoConvergenciaPMO,
        BlocoConfiguracoesExpansaoPMO,
        BlocoMARSPMO,
        BlocoRiscoDeficitENSPMO,
        BlocoCustoOperacaoPMO,
        BlocoCustoOperacaoTotalPMO,
        BlocoProdutibilidadesConfiguracaoPMO,
        BlocoEnergiaArmazenadaMaximaPMO,
        BlocoEnergiaArmazenadaInicialPMO,
        BlocoVolumeArmazenadoInicialPMO,
        BlocoPenalidadeViolacaoOutrosUsosPMO,
        BlocoPenalidadeViolacaoVazaoMinimaPMO,
        BlocoPenalidadeViolacaoCurvaSegurancaPMO,
        BlocoPenalidadeViolacaoFphaPMO,
        BlocoPenalidadeViolacaoEvaporacaoPMO,
        BlocoPenalidadeViolacaoTurbinamentoMaximoPMO,
        BlocoPenalidadeViolacaoTurbinamentoMinimoPMO,
        BlocoGeracaoMinimaUsinasTermicasPMO,
        BlocoGeracaoMaximaUsinasTermicasPMO,
    ]

    @property
    def versao_modelo(self) -> Optional[str]:
        """
        A versão do modelo que produziu o arquivo.

        :return: A string de versão do modelo.
        :rtype: str | None
        """
        b = self.data.get_blocks_of_type(BlocoVersaoModeloPMO)
        if isinstance(b, BlocoVersaoModeloPMO):
            return b.data
        elif isinstance(b, list):
            return b[0].data
        return None

    @property
    def eafpast_tendencia_hidrologica(self) -> Optional[pd.DataFrame]:
        """
        Energias afluentes passadas por REE para análise da tendência
        hidrológica, em relação à primeira configuração do sistema,
        em MWmes.

        - nome_ree (`str`)
        - mes (`int`)
        - valor (`float`)

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

        - nome_ree (`str`)
        - mes (`int`)
        - valor (`float`)

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

        - data (`datetime`)
        - valor (`int`)

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

        - data (`datetime`)
        - valor (`int`)

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

        - data (`datetime`)
        - valor (`int`)

        :return: As configurações em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoConfiguracoesExpansaoPMO)
        if isinstance(b, list):
            return b[2].data
        elif isinstance(b, BlocoConfiguracoesExpansaoPMO):
            return b.data
        return None

    @property
    def energia_armazenada_maxima(self) -> Optional[pd.DataFrame]:
        """
        Valores da energia armazenada máxima para cada REE do caso.

        - nome_ree (`str`)
        - configuracao (`int`)
        - valor_MWmes (`float`)

        :return: As energias em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoEnergiaArmazenadaMaximaPMO)
        if isinstance(b, BlocoEnergiaArmazenadaMaximaPMO):
            return b.data
        return None

    @property
    def energia_armazenada_inicial(self) -> Optional[pd.DataFrame]:
        """
        Valores da energia armazenada inicial para cada REE do caso.

        - nome_ree (`str`)
        - valor_MWmes (`float`)
        - valor_percentual (`float`)

        :return: As energias em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoEnergiaArmazenadaInicialPMO)
        if isinstance(b, BlocoEnergiaArmazenadaInicialPMO):
            return b.data
        return None

    @property
    def volume_armazenado_inicial(self) -> Optional[pd.DataFrame]:
        """
        Valores do volume armazenado inicial para cada UHE do caso.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - valor_hm3 (`float`)
        - valor_percentual (`float`)

        :return: As configurações em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoVolumeArmazenadoInicialPMO)
        if isinstance(b, BlocoVolumeArmazenadoInicialPMO):
            return b.data
        return None

    def retas_perdas_engolimento(self, estagio: int) -> Optional[pd.DataFrame]:
        """
        Retas ajustadas segundo o modelo MARS para corrigir a
        energia fio d'água com as perdas por engolimento máximo.

        - nome_ree (`str`)
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
        - nome_submercado (`str`)
        - risco (`float`)
        - eens (`float`)

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

    @property
    def penalidade_violacao_outros_usos(self) -> Optional[pd.DataFrame]:
        """
        Tabela de penalidades aplicadas à violação de restrições de
        outros usos da água.

        - ree (`str`)
        - data (`datetime`)
        - valor (`float`)

        :return: As penalidades em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoPenalidadeViolacaoOutrosUsosPMO)
        if isinstance(b, BlocoPenalidadeViolacaoOutrosUsosPMO):
            return b.data
        return None

    @property
    def penalidade_violacao_vazao_minima(self) -> Optional[pd.DataFrame]:
        """
        Tabela de penalidades aplicadas à violação de restrições de
        vazão mínima.

        - ree (`str`)
        - data (`datetime`)
        - patamar (`int`)
        - valor (`float`)

        :return: As penalidades em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoPenalidadeViolacaoVazaoMinimaPMO)
        if isinstance(b, BlocoPenalidadeViolacaoVazaoMinimaPMO):
            return b.data
        return None

    @property
    def penalidade_violacao_turbinamento_minimo(
        self,
    ) -> Optional[pd.DataFrame]:
        """
        Tabela de penalidades aplicadas à violação de restrições de
        turbinamento mínimo.

        - data (`datetime`)
        - valor (`float`)

        :return: As penalidades em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(
            BlocoPenalidadeViolacaoTurbinamentoMinimoPMO
        )
        if isinstance(b, BlocoPenalidadeViolacaoTurbinamentoMinimoPMO):
            return b.data
        return None

    @property
    def penalidade_violacao_turbinamento_maximo(
        self,
    ) -> Optional[pd.DataFrame]:
        """
        Tabela de penalidades aplicadas à violação de restrições de
        turbinamento máximo.

        - data (`datetime`)
        - valor (`float`)

        :return: As penalidades em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(
            BlocoPenalidadeViolacaoTurbinamentoMaximoPMO
        )
        if isinstance(b, BlocoPenalidadeViolacaoTurbinamentoMaximoPMO):
            return b.data
        return None

    @property
    def penalidade_violacao_curva(
        self,
    ) -> Optional[pd.DataFrame]:
        """
        Tabela de penalidades aplicadas à violação de restrições de
        curva de segurança.

        - ree (`str`)
        - data (`datetime`)
        - valor (`float`)

        :return: As penalidades em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(
            BlocoPenalidadeViolacaoCurvaSegurancaPMO
        )
        if isinstance(b, BlocoPenalidadeViolacaoCurvaSegurancaPMO):
            return b.data
        return None

    @property
    def penalidade_violacao_fpha(
        self,
    ) -> Optional[pd.DataFrame]:
        """
        Tabela de penalidades aplicadas à violação de restrições da
        FPHA.

        - ree (`str`)
        - data (`datetime`)
        - valor (`float`)

        :return: As penalidades em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoPenalidadeViolacaoFphaPMO)
        if isinstance(b, BlocoPenalidadeViolacaoFphaPMO):
            return b.data
        return None

    @property
    def penalidade_violacao_evaporacao(
        self,
    ) -> Optional[pd.DataFrame]:
        """
        Tabela de penalidades aplicadas à violação de restrições da
        evaporação.

        - ree (`str`)
        - data (`datetime`)
        - valor (`float`)

        :return: As penalidades em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoPenalidadeViolacaoEvaporacaoPMO)
        if isinstance(b, BlocoPenalidadeViolacaoEvaporacaoPMO):
            return b.data
        return None

    @property
    def geracao_minima_usinas_termicas(
        self,
    ) -> Optional[pd.DataFrame]:
        """
        Tabela de geração térmica mínima por usina térmica
        existente no caso.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - data (`datetime`)
        - valor_MWmed (`float`)

        :return: As gerações em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoGeracaoMinimaUsinasTermicasPMO)
        cols = ["codigo_usina", "nome_usina", "data", "valor_MWmed"]
        if isinstance(b, list):
            df = pd.concat([b.data for b in b], ignore_index=True)
            df = df.sort_values(by=["codigo_usina", "data"])
            return df[cols]
        elif isinstance(b, BlocoGeracaoMinimaUsinasTermicasPMO):
            df = b.data.sort_values(by=["codigo_usina", "data"])
            return df[cols]
        return None

    @property
    def geracao_maxima_usinas_termicas(
        self,
    ) -> Optional[pd.DataFrame]:
        """
        Tabela de geração térmica máxima por usina térmica
        existente no caso.

        - codigo_usina (`int`)
        - nome_usina (`str`)
        - data (`datetime`)
        - valor_MWmed (`float`)

        :return: As gerações em um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_blocks_of_type(BlocoGeracaoMaximaUsinasTermicasPMO)
        cols = ["codigo_usina", "nome_usina", "data", "valor_MWmed"]
        if isinstance(b, list):
            df = pd.concat([b.data for b in b], ignore_index=True)
            df = df.sort_values(by=["codigo_usina", "data"])
            return df[cols]
        elif isinstance(b, BlocoGeracaoMaximaUsinasTermicasPMO):
            df = b.data.sort_values(by=["codigo_usina", "data"])
            return df[cols]
        return None
