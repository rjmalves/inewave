from inewave.newave.modelos.simfinal import BlocoVersaoModeloSimfinal
from inewave.newave.modelos.simfinal import BlocoCustoOperacaoSimfinal
from inewave.newave.modelos.simfinal import BlocoCustoOperacaoTotalSimfinal
from cfinterface.files.blockfile import BlockFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class Simfinal(BlockFile):
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
        BlocoVersaoModeloSimfinal,
        BlocoCustoOperacaoSimfinal,
        BlocoCustoOperacaoTotalSimfinal,
    ]

    @property
    def versao_modelo(self) -> Optional[str]:
        """
        A versão do modelo que produziu o arquivo.

        :return: A string de versão do modelo.
        :rtype: str | None
        """
        b = self.data.get_blocks_of_type(BlocoVersaoModeloSimfinal)
        if isinstance(b, BlocoVersaoModeloSimfinal):
            return b.data
        elif isinstance(b, list):
            return b[0].data
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
        b = self.data.get_blocks_of_type(BlocoCustoOperacaoSimfinal)
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
        b = self.data.get_blocks_of_type(BlocoCustoOperacaoSimfinal)
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
        b = self.data.get_blocks_of_type(BlocoCustoOperacaoSimfinal)
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
        b = self.data.get_blocks_of_type(BlocoCustoOperacaoTotalSimfinal)
        if isinstance(b, BlocoCustoOperacaoTotalSimfinal):
            return b.data[0]
        return None

    @property
    def desvio_custo_operacao_total(self) -> Optional[float]:
        """
        O desvio padrão do custo de operacao total da SF.

        :return: O desvio do custo total.
        :rtype: float | None
        """
        b = self.data.get_blocks_of_type(BlocoCustoOperacaoTotalSimfinal)
        if isinstance(b, BlocoCustoOperacaoTotalSimfinal):
            return b.data[1]
        return None
