from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.forwarh import SecaoDadosForwarh


from typing import TypeVar, Optional, List


class Forwarh(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes ao
    cabeçalho dos dados das simulações forward.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosForwarh]
    STORAGE = "BINARY"

    def __bloco_dados(self) -> Optional[SecaoDadosForwarh]:
        dados = [r for r in self.data.of_type(SecaoDadosForwarh)]
        if len(dados) == 1:
            return dados[0]
        else:
            return None

    @property
    def nome_caso(self) -> Optional[str]:
        """
        O nome do caso, conforme cadastrado no `dger.dat`.

        :return: O nome do caso
        :rtype: str
        """
        dados = self.__bloco_dados()
        return dados.nome_caso if dados is not None else None

    @property
    def numero_rees(self) -> Optional[int]:
        """
        O número de REEs cadastrados no `ree.dat`.

        :return: O número de REEs
        :rtype: str
        """
        dados = self.__bloco_dados()
        return dados.numero_rees if dados is not None else None

    @property
    def numero_submercados(self) -> Optional[int]:
        """
        O número de submercados cadastrados no `sistema.dat`.

        :return: O número de submercados
        :rtype: str
        """
        dados = self.__bloco_dados()
        return dados.numero_submercados if dados is not None else None

    @property
    def numero_series_gravadas(self) -> Optional[int]:
        """
        O número de séries gravadas, configurado no `dger.dat`.

        :return: O número de séries gravadas
        :rtype: str
        """
        dados = self.__bloco_dados()
        return dados.numero_series_gravadas if dados is not None else None

    @property
    def numero_aberturas(self) -> Optional[int]:
        """
        O número de aberturas, configurado no `dger.dat`.

        :return: O número de aberturas
        :rtype: str
        """
        dados = self.__bloco_dados()
        return dados.numero_aberturas if dados is not None else None

    @property
    def numero_estagios_estudo(self) -> Optional[int]:
        """
        O número de estágios do período de estudo, configurado no `dger.dat`.

        :return: O número de estágios
        :rtype: str
        """
        dados = self.__bloco_dados()
        return dados.numero_estagios_estudo if dados is not None else None

    @property
    def intervalo_series_gravadas(self) -> Optional[int]:
        """
        O intervalo de espaçamento das séries gravadas, configurado no `dger.dat`.

        :return: O intervalo entre as séries
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return dados.intervalo_series_gravadas if dados is not None else None

    @property
    def numero_classes_termicas_submercados(self) -> Optional[List[int]]:
        """
        O número de classes térmicas por submercado, configurado no `clast.dat`.

        :return: A lista com o número de classes térmicas
        :rtype: list[int] | None
        """
        dados = self.__bloco_dados()
        return (
            dados.numero_classes_termicas_submercados
            if dados is not None
            else None
        )

    @property
    def numero_patamares_deficit(self) -> Optional[int]:
        """
        O número de patamares de déficit, configurado no `sistema.dat`.

        :return: O número de patamares
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return dados.numero_patamares_deficit if dados is not None else None

    @property
    def tamanho_registro_arquivo_forward(self) -> Optional[int]:
        """
        O tamanho de um registro do arquivo forward, em bytes.

        :return: O número de bytes de um registro
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return (
            dados.tamanho_registro_arquivo_forward
            if dados is not None
            else None
        )

    @property
    def numero_registros_arquivo_forward(self) -> Optional[int]:
        """
        O número de registros do arquivo forward.

        :return: O número de registros
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return (
            dados.numero_registros_arquivo_forward
            if dados is not None
            else None
        )

    @property
    def numero_registros_necessarios_estagio(self) -> Optional[int]:
        """
        O número de registros necessários por estágio, no arquivo forward.

        :return: O número de registros por estágio
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return (
            dados.numero_registros_necessarios_estagio
            if dados is not None
            else None
        )

    @property
    def ano_inicio_estudo(self) -> Optional[int]:
        """
        O ano de início do estudo, configurado no arquivo `dger.dat`.

        :return: O ano de início do estudo
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return dados.ano_inicio_estudo if dados is not None else None

    @property
    def ano_inicio_historico_vazoes(self) -> Optional[int]:
        """
        O ano de início do histórico de vazões, configurado no arquivo `dger.dat`.

        :return: O ano de início do histórico
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return dados.ano_inicio_historico_vazoes if dados is not None else None

    @property
    def numero_anos_descontar_historico_vazoes(self) -> Optional[int]:
        """
        O número de anos a descontar do histórico.

        :return: O número de anos
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return (
            dados.numero_anos_descontar_historico_vazoes
            if dados is not None
            else None
        )

    @property
    def numero_estagios_ano(self) -> Optional[int]:
        """
        O número de estágios por ano, configurado através da duração do período
        no `dger.dat`.

        :return: O número de estágios por ano
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return dados.numero_estagios_ano if dados is not None else None

    @property
    def mes_inicio_estudo(self) -> Optional[int]:
        """
        O mês de início do estudo, configurado no `dger.dat`.

        :return: O mês de início do período de estudo
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return dados.mes_inicio_estudo if dados is not None else None

    @property
    def mes_inicio_pre_estudo(self) -> Optional[int]:
        """
        O mês de início do pré-estudo, configurado no `dger.dat`.

        :return: O mês de início do período pré-estudo
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return dados.mes_inicio_pre_estudo if dados is not None else None

    @property
    def numero_estagios_pre_estudo(self) -> Optional[int]:
        """
        O número de estágios pré-estudo.

        :return: O número de estágios pré-estudo
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return dados.numero_estagios_pre_estudo if dados is not None else None

    @property
    def numero_patamares_carga(self) -> Optional[int]:
        """
        O número de patamares de carga, configurado no `patamar.dat`

        :return: O número de patamares
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return dados.numero_patamares_carga if dados is not None else None

    @property
    def ordem_maxima_parp(self) -> Optional[int]:
        """
        A ordem máxima dos modelos PAR(p), configurada no `dger.dat`

        :return: A ordem máxima dos modelos
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return dados.ordem_maxima_parp if dados is not None else None

    @property
    def ano_inicio_series_historicas_simuladas(self) -> Optional[List[int]]:
        """
        O ano de início das séries históricas simuladas, caso seja feita
        simulação histórica.

        :return: A ordem máxima dos modelos
        :rtype: list[int] | None
        """
        dados = self.__bloco_dados()
        return (
            dados.ano_inicio_series_historicas_simuladas
            if dados is not None
            else None
        )

    @property
    def numero_anos_historico_vazoes(self) -> Optional[int]:
        """
        O número de anos existentes no histórico de vazões.

        :return: O número de anos
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return (
            dados.numero_anos_historico_vazoes if dados is not None else None
        )

    @property
    def numero_total_submercados(self) -> Optional[int]:
        """
        O número total de submercados, considerando fictícios, cadastrados
        no `sistema.dat`.

        :return: O número total de submercados
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return dados.numero_total_submercados if dados is not None else None

    @property
    def simulacao_final_individualizada(self) -> Optional[int]:
        """
        O uso de simulação final individualizada, configurado no `dger.dat`.

        :return: O valor do flag de simulação final individualizada
        :rtype: int | None
        """
        dados = self.__bloco_dados()
        return (
            dados.simulacao_final_individualizada
            if dados is not None
            else None
        )
