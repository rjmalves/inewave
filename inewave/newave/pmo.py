from inewave.newave.modelos.pmo import BlocoEafPastTendenciaHidrolPMO
from inewave.newave.modelos.pmo import BlocoEafPastCfugaMedioPMO
from inewave.newave.modelos.pmo import BlocoConvergenciaPMO
from inewave.newave.modelos.pmo import BlocoConfiguracoesExpansaoPMO
from inewave.newave.modelos.pmo import BlocoMARSPMO
from inewave.newave.modelos.pmo import BlocoRiscoDeficitENSPMO
from inewave.newave.modelos.pmo import BlocoCustoOperacaoPMO
from inewave.newave.modelos.pmo import BlocoCustoOperacaoTotalPMO

from cfinterface.components.block import Block
from cfinterface.files.blockfile import BlockFile
from typing import Type, TypeVar, Optional, Any
import pandas as pd  # type: ignore


class PMO(BlockFile):
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
    ]

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="pmo.dat") -> "PMO":
        return cls.read(diretorio, nome_arquivo)

    def __bloco_por_tipo(self, bloco: Type[T], indice: int) -> Optional[T]:
        """
        Obtém um gerador de blocos de um tipo, se houver algum no arquivo.

        :param bloco: Um tipo de bloco para ser lido
        :type bloco: T
        :param indice: O índice do bloco a ser acessado, dentre os do tipo
        :type indice: int
        :return: O gerador de blocos, se houver
        :rtype: Optional[Generator[T], None, None]
        """
        try:
            return next(
                b
                for i, b in enumerate(self.data.of_type(bloco))
                if i == indice
            )
        except StopIteration:
            return None

    def __extrai_dados_se_existe(
        self, bloco: Type[Block], indice: int = 0
    ) -> Optional[Any]:
        """
        Obtém os dados de um bloco se este existir dentre os blocos do arquivo.

        :param bloco: O tipo do bloco cujos dados serão extraídos
        :type bloco: Type[T]
        :param indice: Qual dos blocos do tipo será acessado
        :type indice: int, optional
        :return: Os dados do bloco, se existirem
        :rtype: Any
        """
        b = self.__bloco_por_tipo(bloco, indice)
        if b is not None:
            return b.data
        return None

    # def __atribui_dados_se_existe(
    #     self, bloco: Type[Block], valor: Any, indice: int = 0
    # ):
    #     """
    #     Atribui dados em um bloco existente. Retorna um erro se
    #     o bloco não existir.

    #     :param bloco: O tipo do bloco cujos dados serão extraídos
    #     :type bloco: Type[T]
    #     :param valor: O valor a ser atribuído
    #     :type valor: Any
    #     :param indice: Qual dos blocos do tipo será acessado
    #     :type indice: int, optional
    #     """
    #     b = self.__bloco_por_tipo(bloco, indice)
    #     if b is not None:
    #         b.data = valor
    #     else:
    #         raise ValueError(
    #             f"Bloco do tipo {bloco.__name__} na posição"
    #             + f" {indice} não encontrado"
    #         )

    @property
    def eafpast_tendencia_hidrologica(self) -> Optional[pd.DataFrame]:
        """
        Energias afluentes passadas por REE para análise da tendência
        hidrológica, em relação à primeira configuração do sistema,
        em MWmes.

        **Retorna**

        `Optional[pd.DataFrame]`
        """
        return self.__extrai_dados_se_existe(BlocoEafPastTendenciaHidrolPMO)

    # @eafpast_tendencia_hidrologica.setter
    # def eafpast_tendencia_hidrologica(self, eaf: pd.DataFrame):
    #     self.__atribui_dados_se_existe(BlocoEafPastTendenciaHidrolPMO, eaf)

    @property
    def eafpast_cfuga_medio(self) -> Optional[pd.DataFrame]:
        """
        Energias afluentes passadas por REE considerando canal de
        fuga médio, em relação à primeira configuração do sistema,
        em MWmes.

        **Retorna**

        `Optional[pd.DataFrame]`
        """
        return self.__extrai_dados_se_existe(BlocoEafPastCfugaMedioPMO)

    # @eafpast_cfuga_medio.setter
    # def eafpast_cfuga_medio(self, eaf: pd.DataFrame):
    #     self.__atribui_dados_se_existe(BlocoEafPastCfugaMedioPMO, eaf)

    @property
    def configuracoes_entrada_reservatorio(self) -> Optional[pd.DataFrame]:
        """
        Configurações do sistema em cada período devido a entrada
        de reservatórios e/ou potência de base.

        **Retorna**

        `Optional[pd.DataFrame]`
        """
        return self.__extrai_dados_se_existe(BlocoConfiguracoesExpansaoPMO, 0)

    # @configuracoes_entrada_reservatorio.setter
    # def configuracoes_entrada_reservatorio(self, cfg: pd.DataFrame):
    #     self.__atribui_dados_se_existe(BlocoConfiguracoesExpansaoPMO, cfg, 0)

    @property
    def configuracoes_alteracao_potencia(self) -> Optional[pd.DataFrame]:
        """
        Configurações do sistema em cada período devido a alterações
        de potência.

        **Retorna**

        `Optional[pd.DataFrame]`
        """
        return self.__extrai_dados_se_existe(BlocoConfiguracoesExpansaoPMO, 1)

    # @configuracoes_alteracao_potencia.setter
    # def configuracoes_alteracao_potencia(self, cfg: pd.DataFrame):
    #     self.__atribui_dados_se_existe(BlocoConfiguracoesExpansaoPMO, cfg, 1)

    @property
    def configuracoes_qualquer_modificacao(self) -> Optional[pd.DataFrame]:
        """
        Configurações do sistema em cada período devido a alterações
        de potência.

        **Retorna**

        `Optional[pd.DataFrame]`
        """
        return self.__extrai_dados_se_existe(BlocoConfiguracoesExpansaoPMO, 2)

    # @configuracoes_qualquer_modificacao.setter
    # def configuracoes_qualquer_modificacao(self, cfg: pd.DataFrame):
    #     self.__atribui_dados_se_existe(BlocoConfiguracoesExpansaoPMO, cfg, 2)

    def retas_perdas_engolimento(self, estagio: int) -> Optional[pd.DataFrame]:
        """
        Retas ajustadas segundo o modelo MARS para corrigir a
        energia fio d'água com as perdas por engolimento máximo.

        **Retorna**

        `Optional[pd.DataFrame]`
        """
        return self.__extrai_dados_se_existe(BlocoMARSPMO, estagio - 1)

    @property
    def convergencia(self) -> Optional[pd.DataFrame]:
        """
        Tabela de convergência da execução do NEWAVE.

        **Retorna**

        `Optional[pd.DataFrame]`
        """
        return self.__extrai_dados_se_existe(BlocoConvergenciaPMO)

    @property
    def risco_deficit_ens(self) -> Optional[pd.DataFrame]:
        """
        Tabela de riscos de déficit e enegia não suprida (ENS).

        **Retorna**

        `Optional[pd.DataFrame]`
        """
        return self.__extrai_dados_se_existe(BlocoRiscoDeficitENSPMO)

    @property
    def custo_operacao_series_simuladas(self) -> Optional[pd.DataFrame]:
        """
        Tabela de custos de operação categorizados para as
        séries simuladas.

        **Retorna**

        `Optional[pd.DataFrame]`
        """
        return self.__extrai_dados_se_existe(BlocoCustoOperacaoPMO, 0)

    @property
    def valor_esperado_periodo_estudo(self) -> Optional[pd.DataFrame]:
        """
        Tabela de custos de operação esperados para o período
        de estudo.

        **Retorna**

        `Optional[pd.DataFrame]`
        """
        return self.__extrai_dados_se_existe(BlocoCustoOperacaoPMO, 1)

    @property
    def custo_operacao_referenciado_primeiro_mes(
        self,
    ) -> Optional[pd.DataFrame]:
        """
        Tabela de custos de operação esperados para o período
        de estudo, referenciados ao primeiro mês.

        **Retorna**

        `Optional[pd.DataFrame]`
        """
        return self.__extrai_dados_se_existe(BlocoCustoOperacaoPMO, 2)

    @property
    def custo_operacao_total(self) -> Optional[float]:
        """
        Custo de operacao total da SF.

        **Retorna**

        `Optional[float]`
        """
        b = self.__extrai_dados_se_existe(BlocoCustoOperacaoTotalPMO)
        if isinstance(b, list):
            return b[0]
        return None

    @property
    def desvio_custo_operacao_total(self) -> Optional[float]:
        """
        Custo de operacao total da SF.

        **Retorna**

        `Optional[float]`
        """
        b = self.__extrai_dados_se_existe(BlocoCustoOperacaoTotalPMO)
        if isinstance(b, list):
            return b[1]
        return None
