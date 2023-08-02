from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.forward import VariavelOperacao, SecaoDadosForward


from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class Forward(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes às simulações
    forward.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosForward]
    STORAGE = "BINARY"

    def __bloco_dados(self) -> Optional[SecaoDadosForward]:
        dados = [r for r in self.data.of_type(SecaoDadosForward)]
        if len(dados) == 1:
            return dados[0]
        else:
            return None

    def __dados_variavel(self, variavel: VariavelOperacao) -> pd.DataFrame:
        dados = self.__bloco_dados()
        if dados is not None:
            return (
                dados.data.get(variavel)
                if dados is not None
                else pd.DataFrame()
            )
        else:
            return pd.DataFrame()

    @property
    def mercado_liquido(self) -> pd.DataFrame:
        """
        A tabela com os valores do mercado líquido de energia
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - submercado (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.MERCADO)

    @property
    def energia_armazenada_absoluta_inicial(self) -> pd.DataFrame:
        """
        A tabela com os valores do EARM inicial do estágio
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_INICIAL
        )

    @property
    def energia_natural_afluente(self) -> pd.DataFrame:
        """
        A tabela com os valores de ENA
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_INICIAL
        )

    @property
    def geracao_hidraulica_controlavel(self) -> pd.DataFrame:
        """
        A tabela com os valores de GH controlável
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.GERACAO_HIDRAULICA_CONTROLAVEL
        )

    @property
    def energia_vertida(self) -> pd.DataFrame:
        """
        A tabela com os valores de energia vertida
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.ENERGIA_VERTIDA)

    @property
    def energia_armazenada_absoluta_final(self) -> pd.DataFrame:
        """
        A tabela com os valores do EARM final do estágio
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.ENERGIA_ARMAZENADA_ABSOLUTA_FINAL
        )

    @property
    def energia_natural_afluente_fio_bruta(self) -> pd.DataFrame:
        """
        A tabela com os valores de ENA fio d'água bruta
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO_BRUTA
        )

    @property
    def energia_evaporada(self) -> pd.DataFrame:
        """
        A tabela com os valores de energia evaporada
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.ENERGIA_EVAPORADA)

    @property
    def energia_enchimento_volume_morto(self) -> pd.DataFrame:
        """
        A tabela com os valores de energia de enchimento de volume morto
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.ENERGIA_ENCHIMENTO_VOLUME_MORTO
        )

    @property
    def geracao_termica(self) -> pd.DataFrame:
        """
        A tabela com os valores de geração térmica
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.GERACAO_TERMICA)

    @property
    def deficit(self) -> pd.DataFrame:
        """
        A tabela com os valores de déficit
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - submercado (`str`)
        - patamarDeficit (`int`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.DEFICIT)

    @property
    def valor_agua(self) -> pd.DataFrame:
        """
        A tabela com os valores da água (multiplicadores duais
        da restrição de balanço hídrico) para cada série, em R$/MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.VALOR_AGUA)

    @property
    def custo_marginal_operacao(self) -> pd.DataFrame:
        """
        A tabela com os custos marginais de operação (multiplicadores duais
        da restrição de balanço de demanda) para cada série, em R$/MWh.

        - estagio (`int`)
        - cenario (`int`)
        - submercado (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.CUSTO_MARGINAL_OPERACAO)

    @property
    def geracao_hidraulica_fio_liquida(self) -> pd.DataFrame:
        """
        A tabela com os valores de geração hidráulica fio líquida
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.GERACAO_HIDRAULICA_FIO_LIQUIDA
        )

    @property
    def perdas_geracao_hidraulica_fio(self) -> pd.DataFrame:
        """
        A tabela com os valores de perdas na geração hidráulica fio
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.PERDAS_GERACAO_HIDRAULICA_FIO
        )

    @property
    def intercambio(self) -> pd.DataFrame:
        """
        A tabela com os valores de intercâmbio
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - submercadoDe (`str`)
        - submercadoPara (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.INTERCAMBIO)

    @property
    def excesso(self) -> pd.DataFrame:
        """
        A tabela com os valores de excesso
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - submercado (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.EXCESSO)

    @property
    def energia_natural_afluente_bruta(self) -> pd.DataFrame:
        """
        A tabela com os valores de ENA bruta
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_BRUTA
        )

    @property
    def energia_natural_afluente_controlavel_corrigida(self) -> pd.DataFrame:
        """
        A tabela com os valores de ENA controlável corrigida
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL_CORRIGIDA
        )

    @property
    def geracao_hidraulica_maxima(self) -> pd.DataFrame:
        """
        A tabela com os valores de geração hidráulica máxima
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA
        )

    @property
    def energia_afluente_controlavel_desvio(self) -> pd.DataFrame:
        """
        A tabela com os valores de energia afluente controlável
        de desvio para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO
        )

    @property
    def energia_afluente_fio_desvio(self) -> pd.DataFrame:
        """
        A tabela com os valores de energia afluente fio de desvio
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.ENERGIA_AFLUENTE_FIO_DESVIO
        )

    @property
    def beneficio_intercambio(self) -> pd.DataFrame:
        """
        A tabela com os valores de benefício de intercâmbio
        para cada série, em R$/MWh.

        - estagio (`int`)
        - cenario (`int`)
        - submercadoDe (`str`)
        - submercadoPara (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.BENEFICIO_INTERCAMBIO)

    @property
    def fator_correcao_energia_natural_afluente_controlavel(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores dos fatores de correção para a
        energia natural afluente controlável
        para cada série, adimensionais.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.FATOR_CORRECAO_ENERGIA_NATURAL_AFLUENTE_CONTROLAVEL
        )

    @property
    def violacao_curva_aversao(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação da curva de aversão
        de volume mínimo operativo para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.VIOLACAO_CURVA_AVERSAO)

    @property
    def acionamento_curva_aversao(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com o acionamento da curva de aversão
        de volume mínimo operativo para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.ACIONAMENTO_CURVA_AVERSAO
        )

    @property
    def penalidade_curva_aversao(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com a penalidade por violação da curva de aversão
        de volume mínimo operativo para cada série, em R$.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.PENALIDADE_CURVA_AVERSAO)

    @property
    def custo_operacao(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com o custo total de operação para cada série, em 10^3 * R$.

        - estagio (`int`)
        - cenario (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.CUSTO_OPERACAO)

    @property
    def custo_geracao_termica(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com o custo de geração térmica para cada série, em 10^3 * R$.

        - estagio (`int`)
        - cenario (`int`)
        - submercado (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.CUSTO_GERACAO_TERMICA)

    @property
    def beneficio_agrupamento_intercambio(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com o benefício do agrupamento dos intercâmbios
        para cada série, em R$/MWh.

        - estagio (`int`)
        - cenario (`int`)
        - agrupamentoIntercambio (`int`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.BENEFICIO_AGRUPAMENTO_INTERCAMBIO
        )

    @property
    def energia_natural_afluente_fio(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de ENA fio
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.ENERGIA_NATURAL_AFLUENTE_FIO
        )

    @property
    def beneficio_despacho_gnl(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com o benefício do despacho térmico GNL
        para cada série, em R$/MWh.

        - estagio (`int`)
        - cenario (`int`)
        - lag (`int`)
        - patamar (`int`)
        - submercado (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.BENEFICIO_DESPACHO_GNL)

    @property
    def violacao_geracao_hidraulica_minima(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação da geração hidráulica mínima
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VIOLACAO_GERACAO_HIRAULICA_MINIMA
        )

    @property
    def violacao_energia_vazao_minima(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores da energia de vazão mínima
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VIOLACAO_ENERGIA_VAZAO_MINIMA
        )

    @property
    def geracao_hidraulica_maxima_considerando_restricoes_eletricas(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores da geração hidráulica máxima considerando
        restrições elétricas para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.GERACAO_HIDRAULICA_MAXIMA_CONSIDERANDO_RE
        )

    @property
    def volume_armazenado_absoluto_final(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de volume armazenado por usina
        para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_FINAL
        )

    @property
    def geracao_hidraulica_usina(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de geração hidráulica por usina
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.GERACAO_HIDRAULICA_USINA)

    @property
    def volume_turbinado(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de volume turbinado por usina
        para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.VOLUME_TURBINADO)

    @property
    def volume_vertido(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de volume vertido por usina
        para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.VOLUME_VERTIDO)

    @property
    def violacao_geracao_hidraulica_minima_usina(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação de geração hidráulica mínima
        por usina para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VIOLACAO_GERACAO_HIDRAULICA_MINIMA_USINA
        )

    @property
    def enchimento_volume_morto_usina(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de enchimento de volume morto
        por usina para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.ENCHIMENTO_VOLUME_MORTO_USINA
        )

    @property
    def violacao_defluencia_minima(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação de restrições de
        defluência mínima por usina para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VIOLACAO_DEFLUENCIA_MINIMA
        )

    @property
    def volume_desvio_usina(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de volume de desvio
        por usina para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.VOLUME_DESVIO_USINA)

    @property
    def volume_desvio_positivo_usina(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de volume de desvio positivo
        por usina para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VOLUME_DESVIO_POSITIVO_USINA
        )

    @property
    def volume_desvio_negativo_usina(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de volume de desvio negativo
        por usina para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VOLUME_DESVIO_NEGATIVO_USINA
        )

    @property
    def violacao_fpha(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação de restrições da
        FPHA por usina para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.VIOLACAO_FPHA)

    @property
    def vazao_afluente(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de vazão afluente
        por usina para cada série, em m3/s.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.VAZAO_AFLUENTE)

    @property
    def vazao_incremental(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de vazão incremental
        por usina para cada série, em m3/s.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.VAZAO_INCREMENTAL)

    @property
    def volume_armazenado_percentual_final(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de volume armazenado final
        por usina para cada série, em % do volume máximo.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VOLUME_ARMAZENADO_PERCENTUAL_FINAL
        )

    @property
    def custo_violacao_energia_vazao_minima(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de custo de violação das restrições
        de energia da vazão mínima
        para cada série, em 10^3 R$.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.CUSTO_VIOLACAO_ENERGIA_VAZAO_MINIMA
        )

    @property
    def custo_energia_afluente_controlavel_desvio(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de custo da violação da meta de
        desvio da energia afluente controlável
        para cada série, em 10^3 R$.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_CONTROLAVEL_DESVIO
        )

    @property
    def custo_energia_afluente_fio_desvio(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de custo da violação da meta de
        desvio da energia afluente fio
        para cada série, em 10^3 R$.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.CUSTO_ENERGIA_AFLUENTE_FIO_DESVIO
        )

    @property
    def custo_violacao_geracao_hidraulica_minima(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de custo da violação da geração
        hidráulica mínima
        para cada série, em 10^3 R$.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.CUSTO_VIOLACAO_GERACAO_HIDRAULICA_MINIMA
        )

    @property
    def geracao_eolica(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de geração eólica
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - pee (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.GERACAO_EOLICA)

    @property
    def velocidade_vento(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de velocidade do vento
        para cada série, em m/s.

        - estagio (`int`)
        - cenario (`int`)
        - pee (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.VELOCIDADE_VENTO)

    @property
    def violacao_funcao_producao_eolica(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação da função de produção
        eólica para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - pee (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VIOLACAO_FUNCAO_PRODUCAO_EOLICA
        )

    @property
    def violacao_defluencia_maxima(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação de restrições de
        defluência máxima para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VIOLACAO_DEFLUENCIA_MAXIMA
        )

    @property
    def violacao_turbinamento_maximo(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação de restrições de
        turbinamento máximo para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VIOLACAO_TURBINAMENTO_MAXIMO
        )

    @property
    def violacao_turbinamento_minimo(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação de restrições de
        turbinamento mínimo para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VIOLACAO_TURBINAMENTO_MINIMO
        )

    @property
    def violacao_lpp_turbinamento_maximo(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação de restrições LPP de
        turbinamento máximo para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO
        )

    @property
    def violacao_lpp_defluencia_maxima(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação de restrições LPP de
        defluência máxima para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA
        )

    @property
    def violacao_lpp_turbinamento_maximo_usina(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação de restrições LPP de
        turbinamento máximo por usina para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VIOLACAO_LPP_TURBINAMENTO_MAXIMO_USINA
        )

    @property
    def violacao_lpp_defluencia_maxima_usina(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação de restrições LPP de
        defluência máxima por usina para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VIOLACAO_LPP_DEFLUENCIA_MAXIMA_USINA
        )

    @property
    def rhs_lpp_turbinamento_maximo(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores do RHS de restrições LPP de
        turbinamento máximo para cada série, em 10^3 R$.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO
        )

    @property
    def rhs_lpp_defluencia_maxima(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores do RHS de restrições LPP de
        defluência máxima para cada série, em 10^3 R$.

        - estagio (`int`)
        - cenario (`int`)
        - ree (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA
        )

    @property
    def rhs_lpp_turbinamento_maximo_usina(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores do RHS de restrições LPP de
        turbinamento máximo por usina para cada série, em 10^3 R$.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.RHS_LPP_TURBINAMENTO_MAXIMO_USINA
        )

    @property
    def rhs_lpp_defluencia_maxima_usina(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores do RHS de restrições LPP de
        defluência máxima por usina para cada série, em 10^3 R$.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.RHS_LPP_DEFLUENCIA_MAXIMA_USINA
        )

    @property
    def violacao_restricoes_eletricas_especiais(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de violação de
        restrições elétricas especiais para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - restricao (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VIOLACAO_RESTRICOES_ELETRICAS_ESPECIAIS
        )

    @property
    def custo_restricoes_eletricas_especiais(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de custo de violação de
        restrições elétricas especiais para cada série, em 10^3 R$.

        - estagio (`int`)
        - cenario (`int`)
        - restricao (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.CUSTO_RESTRICOES_ELETRICAS_ESPECIAIS
        )

    @property
    def volume_armazenado_absoluto_inicial(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores de volume armazenado inicial
        por usina para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VOLUME_ARMAZENADO_ABSOLUTO_INICIAL
        )

    @property
    def valor_agua_usina(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os valores da água (multiplicadores duais
        da restrição de balanço hídrico) por usina para cada série,
        em R$/hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.VALOR_AGUA_USINA)

    @property
    def volume_evaporado(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os volumes evaporados por usina para cada série,
        em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.VOLUME_EVAPORADO)

    @property
    def volume_bombeado(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os volumes bombeados por estação de bombeamento
        para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - estacao (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(VariavelOperacao.VOLUME_BOMBEADO)

    @property
    def consumo_energia_estacao_bombeamento(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os consumos de energia por estação de bombeamento
        para cada série, em MWmes.

        - estagio (`int`)
        - cenario (`int`)
        - estacao (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.CONSUMO_ENERGIA_ESTACAO_BOMBEAMENTO
        )

    @property
    def volume_canal_desvio_usina(
        self,
    ) -> pd.DataFrame:
        """
        A tabela com os volumes de devio por canal de desvio
        para cada série, em hm3.

        - estagio (`int`)
        - cenario (`int`)
        - usina (`str`)
        - patamar (`int`)
        - valor (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame
        """
        return self.__dados_variavel(
            VariavelOperacao.VOLUME_CANAL_DESVIO_USINA
        )
