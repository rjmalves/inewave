from typing import TypeVar, List, Optional, Union, Type
from datetime import datetime
import pandas as pd  # type: ignore
from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.libs.modelos.eolica import (
    RegistroPEECadastro,
    RegistroPEEPotenciaInstaladaPeriodo,
    RegistroPEEConfiguracaoPeriodo,
    RegistroPEEFTE,
    RegistroPEEGeracaoPatamar,
    RegistroHistoricoVentoHorizonte,
    RegistroHistoricoVento,
    RegistroPEEPostoVento,
    RegistroPostoVentoCadastro,
    RegistroPEESubmercado,
)


class Eolica(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao dados
    das usinas eólicas do sistema.
    """

    T = TypeVar("T", bound=Register)

    REGISTERS = [
        RegistroPEECadastro,
        RegistroPEEPotenciaInstaladaPeriodo,
        RegistroPEEConfiguracaoPeriodo,
        RegistroPEEFTE,
        RegistroPEEGeracaoPatamar,
        RegistroHistoricoVentoHorizonte,
        RegistroHistoricoVento,
        RegistroPEEPostoVento,
        RegistroPostoVentoCadastro,
        RegistroPEESubmercado,
    ]

    def __registros_ou_df(
        self, t: Type[T], **kwargs
    ) -> Optional[Union[T, List[T], pd.DataFrame]]:
        if kwargs.get("df"):
            return self._as_df(t)
        else:
            kwargs_sem_df = {k: v for k, v in kwargs.items() if k != "df"}
            return self.data.get_registers_of_type(t, **kwargs_sem_df)

    def pee_cad(
        self,
        codigo_pee: Optional[int] = None,
        nome_pee: Optional[str] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroPEECadastro, List[RegistroPEECadastro], pd.DataFrame]
    ]:
        """
        Obtém um registro que cadastra um PEE.

        :param codigo_pee: código que especifica o PEE
        :type codigo_pee: int | None
        :param nome_pee: nome do PEE
        :type nome_pee: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEECadastro` |
            list[:class:`RegistroPEECadastro`] | None
        """
        return self.__registros_ou_df(
            RegistroPEECadastro,
            codigo_pee=codigo_pee,
            nome_pee=nome_pee,
            df=df,
        )

    def pee_pot_inst_per(
        self,
        codigo_pee: Optional[int] = None,
        data_inicio: Optional[datetime] = None,
        data_fim: Optional[datetime] = None,
        potencia_instalada: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroPEEPotenciaInstaladaPeriodo,
            List[RegistroPEEPotenciaInstaladaPeriodo],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém a potência instalada por período
        para um PEE.

        :param codigo_pee: código que especifica o PEE
        :type codigo_pee: int | None
        :param data_inicio: período de início de operação
        :type data_inicio: datetime | None
        :param data_fim: período de fim de operação
        :type data_fim: datetime | None
        :param potencia_instalada: potência efetiva do PEE
        :type potencia_instalada: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEEPotenciaInstaladaPeriodo` |
            list[:class:`RegistroPEEPotenciaInstaladaPeriodo`] | None
        """
        return self.__registros_ou_df(
            RegistroPEEPotenciaInstaladaPeriodo,
            codigo_pee=codigo_pee,
            data_inicio=data_inicio,
            data_fim=data_fim,
            potencia_instalada=potencia_instalada,
            df=df,
        )

    def pee_config_per(
        self,
        codigo_pee: Optional[int] = None,
        data_inicio: Optional[datetime] = None,
        data_fim: Optional[datetime] = None,
        estado_operacao: Optional[str] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroPEEConfiguracaoPeriodo,
            List[RegistroPEEConfiguracaoPeriodo],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém a configuração de operação para
        um PEE em um período.

        :param codigo_pee: código que especifica o PEE
        :type codigo_pee: int | None
        :param data_inicio: período de início da configuração
        :type data_inicio: datetime | None
        :param data_fim: período de fim da configuração
        :type data_fim: datetime | None
        :param estado_operacao: tipo de operação
        :type estado_operacao: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEEConfiguracaoPeriodo` |
            list[:class:`RegistroPEEConfiguracaoPeriodo`] | None
        """
        return self.__registros_ou_df(
            RegistroPEEConfiguracaoPeriodo,
            codigo_pee=codigo_pee,
            data_inicio=data_inicio,
            data_fim=data_fim,
            estado_operacao=estado_operacao,
            df=df,
        )

    def pee_fpvp_lin_pu_per(
        self,
        codigo_pee: Optional[int] = None,
        data_inicio: Optional[datetime] = None,
        data_fim: Optional[datetime] = None,
        coeficiente_linear: Optional[float] = None,
        coeficiente_angular: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[RegistroPEEFTE, List[RegistroPEEFTE], pd.DataFrame]]:
        """
        Obtém um registro que contém a função de produção vento-geração
        para um período de tempo para um PEE, em p.u.

        :param codigo_pee: código que especifica o PEE
        :type codigo_pee: int | None
        :param data_inicio: a data inicial de validade para a função
        :type data_inicio: datetime | None
        :param data_fim: a data final de validade para a função
        :type data_fim: datetime | None
        :param coeficiente_linear: o coeficiente linear
        :type coeficiente_linear: float | None
        :param coeficiente_angular: o coeficiente angular
        :type coeficiente_angular: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEEFTE` |
            list[:class:`RegistroPEEFTE`] | None
        """
        return self.__registros_ou_df(
            RegistroPEEFTE,
            codigo_pee=codigo_pee,
            data_inicio=data_inicio,
            data_fim=data_fim,
            coeficiente_linear=coeficiente_linear,
            coeficiente_angular=coeficiente_angular,
            df=df,
        )

    def pee_ger_prof_per_pat(
        self,
        codigo_pee: Optional[int] = None,
        data_inicio: Optional[datetime] = None,
        data_fim: Optional[datetime] = None,
        indice_patamar: Optional[int] = None,
        profundidade: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroPEEGeracaoPatamar,
            List[RegistroPEEGeracaoPatamar],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém a profundidade de um patamar
        de geração para um período, para um PEE.

        :param codigo_pee: código do PEE
        :type codigo_pee: int | None
        :param data_inicio: data de início do registro histórico
        :type data_inicio: datetime | None
        :param data_fim: data de fim do registro histórico
        :type data_fim: datetime | None
        :param indice_patamar: patamar de geração eólica
        :type indice_patamar: int | None
        :param profundidade: profundidade do patamar de geração
        :type profundidade: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEEGeracaoPatamar` |
            list[:class:`RegistroPEEGeracaoPatamar`] | None
        """
        return self.__registros_ou_df(
            RegistroPEEGeracaoPatamar,
            codigo_pee=codigo_pee,
            data_inicio=data_inicio,
            data_fim=data_fim,
            indice_patamar=indice_patamar,
            profundidade=profundidade,
            df=df,
        )

    def vento_hist_horiz(
        self,
        data_inicio: Optional[datetime] = None,
        data_fim: Optional[datetime] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroHistoricoVentoHorizonte,
            List[RegistroHistoricoVentoHorizonte],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém o horizonte de um histórico.

        :param data_inicio: data de início do histórico
        :type data_inicio: datetime | None
        :param data_fim: data de fim do histórico
        :type data_fim: datetime | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroHistoricoVentoHorizonte` |
            list[:class:`RegistroHistoricoVentoHorizonte`] | None
        """
        return self.__registros_ou_df(
            RegistroHistoricoVentoHorizonte,
            data_inicio=data_inicio,
            data_fim=data_fim,
            df=df,
        )

    def vento_hist(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicio: Optional[datetime] = None,
        data_fim: Optional[datetime] = None,
        velocidade: Optional[float] = None,
        direcao: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroHistoricoVento, List[RegistroHistoricoVento], pd.DataFrame
        ]
    ]:
        """
        Obtém um registro que contém a o valor de vento para um
        intervalo do histórico.

        :param codigo_eolica: código da usina eólica
        :type codigo_eolica: int | None
        :param data_inicio: data de início do registro histórico
        :type data_inicio: datetime | None
        :param data_fim: data de fim do registro histórico
        :type data_fim: datetime | None
        :param velocidade: velocidade do vento
        :type velocidade: float | None
        :param direcao: direção do vento
        :type direcao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroHistoricoVento` |
            list[:class:`RegistroHistoricoVento`] | None
        """
        return self.__registros_ou_df(
            RegistroHistoricoVento,
            codigo_eolica=codigo_eolica,
            data_inicio=data_inicio,
            data_fim=data_fim,
            velocidade=velocidade,
            direcao=direcao,
            df=df,
        )

    def posto_vento_cad(
        self,
        codigo_posto: Optional[int] = None,
        nome_posto: Optional[str] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroPostoVentoCadastro,
            List[RegistroPostoVentoCadastro],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que contém o cadastro de um posto
            de vento.

        :param codigo_posto: código que identifica o posto
        :type codigo_posto: int | None
        :param nome_posto: nome do posto de vento
        :type nome_posto: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPostoVentoCadastro` |
            list[:class:`RegistroPostoVentoCadastro`] | None
        """
        return self.__registros_ou_df(
            RegistroPostoVentoCadastro,
            codigo_posto=codigo_posto,
            nome_posto=nome_posto,
            df=df,
        )

    def pee_posto(
        self,
        codigo_pee: Optional[datetime] = None,
        codigo_posto: Optional[datetime] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroPEEPostoVento, List[RegistroPEEPostoVento], pd.DataFrame]
    ]:
        """
        Obtém um registro que contém o mapeamento entre um posto
            e um PEE.

        :param codigo_pee: código que identifica o PEE
        :type codigo_pee: int | None
        :param codigo_posto: código que identifica o posto
        :type codigo_posto: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEEPostoVento` |
            list[:class:`RegistroPEEPostoVento`] | None
        """
        return self.__registros_ou_df(
            RegistroPEEPostoVento,
            codigo_pee=codigo_pee,
            codigo_posto=codigo_posto,
            df=df,
        )

    def pee_subm(
        self,
        codigo_pee: Optional[int] = None,
        codigo_submercado: Optional[int] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroPEESubmercado, List[RegistroPEESubmercado], pd.DataFrame]
    ]:
        """
        Obtém um registro que contém o mapeamento PEE-submercado.

        :param codigo_pee: código que especifica o PEE
        :type codigo_pee: int | None
        :param codigo_submercado: código que especifica o submercado
        :type codigo_submercado: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEESubmercado` |
            list[:class:`RegistroPEESubmercado`] | None
        """
        return self.__registros_ou_df(
            RegistroPEESubmercado,
            codigo_pee=codigo_pee,
            codigo_submercado=codigo_submercado,
            df=df,
        )
