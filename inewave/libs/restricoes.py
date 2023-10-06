from typing import Type, TypeVar, List, Optional, Union
from datetime import datetime
import pandas as pd  # type: ignore
from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.libs.modelos.restricoes import (
    RegistroRE,
    RegistroREHorizPer,
    RegistroRELimFormPer,
    RegistroRHE,
    RegistroRHEHorizPer,
    RegistroRHELsLPPEarmi,
    RegistroRHQ,
    RegistroRHQHorizPer,
    RegistroRHQLsLPPVoli,
    RegistroRHQLimFormPerPat,
    RegistroRHV,
    RegistroRHVHorizPer,
    RegistroRHVLimFormPerPat,
)


class Restricoes(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos dados
    das restrições do problema.
    """

    T = TypeVar("T", bound=Register)

    REGISTERS = [
        RegistroRELimFormPer,
        RegistroREHorizPer,
        RegistroRE,
        RegistroRHELsLPPEarmi,
        RegistroRHEHorizPer,
        RegistroRHE,
        RegistroRHQLimFormPerPat,
        RegistroRHQLsLPPVoli,
        RegistroRHQHorizPer,
        RegistroRHQ,
        RegistroRHVLimFormPerPat,
        RegistroRHVHorizPer,
        RegistroRHV,
    ]

    def __registros_ou_df(
        self, t: Type[T], **kwargs
    ) -> Optional[Union[T, List[T], pd.DataFrame]]:
        if kwargs.get("df"):
            return self._as_df(t)
        else:
            kwargs_sem_df = {k: v for k, v in kwargs.items() if k != "df"}
            return self.data.get_registers_of_type(t, **kwargs_sem_df)

    def re(
        self,
        codigo_restricao: Optional[int] = None,
        formula: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[RegistroRE, List[RegistroRE], pd.DataFrame]]:
        """
        Obtém um registro que cadastra uma usina restrição elétrica (RE).

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param formula: equação da restrição
        :type formula: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRE` |
            list[:class:`RegistroRE`] | `pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroRE,
            codigo_restricao=codigo_restricao,
            formula=formula,
            df=df,
        )

    def re_horiz_per(
        self,
        codigo_restricao: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroREHorizPer, List[RegistroREHorizPer], pd.DataFrame]
    ]:
        """
        Obtém um registro que cadastra o horizonte de validade de uma
        restrição elétrica.

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param data_inicial: data inicial de validade da restrição
        :type data_inicial: datetime | None
        :param data_final: data final de validade da restrição
        :type data_final: datetime | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroREHorizPer` |
            list[:class:`RegistroREHorizPer`] | `pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroREHorizPer,
            codigo_restricao=codigo_restricao,
            data_inicial=data_inicial,
            data_final=data_final,
            df=df,
        )

    def re_lim_form_per(
        self,
        codigo_restricao: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        patamar: Optional[int] = None,
        limite_inferior: Optional[float] = None,
        limite_superior: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroRELimFormPer, List[RegistroRELimFormPer], pd.DataFrame]
    ]:
        """
        Obtém um registro que cadastra os limites por horizonte e por
        patamar para uma restrição elétrica.

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param data_inicial: data inicial de validade dos limites
        :type data_inicial: datetime | None
        :param data_final: data final de validade dos limites
        :type data_final: datetime | None
        :param patamar: patamar de validade dos limites
        :type patamar: int | None
        :param limite_inferior: limite inferior da restrição
        :type limite_inferior: float | None
        :param limite_superior: limite superior da restrição
        :type limite_superior: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRELimFormPer` |
            list[:class:`RegistroRELimFormPer`] | `pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroRELimFormPer,
            codigo_restricao=codigo_restricao,
            data_inicial=data_inicial,
            data_final=data_final,
            patamar=patamar,
            limite_inferior=limite_inferior,
            limite_superior=limite_superior,
            df=df,
        )

    def rhe(
        self,
        codigo_restricao: Optional[int] = None,
        formula: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[RegistroRHE, List[RegistroRHE], pd.DataFrame]]:
        """
        Obtém um registro que cadastra uma usina restrição linear por
        partes de energia (REE).

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param formula: equação da restrição
        :type formula: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHE` |
            list[:class:`RegistroRHE`] | `pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroRHE,
            codigo_restricao=codigo_restricao,
            formula=formula,
            df=df,
        )

    def rhe_horiz_per(
        self,
        codigo_restricao: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroRHEHorizPer, List[RegistroRHEHorizPer], pd.DataFrame]
    ]:
        """
        Obtém um registro que cadastra o horizonte de validade de uma
        restrição linear por partes de energia.

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param data_inicial: data inicial de validade da restrição
        :type data_inicial: datetime | None
        :param data_final: data final de validade da restrição
        :type data_final: datetime | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHEHorizPer` |
            list[:class:`RegistroRHEHorizPer`] | `pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroRHEHorizPer,
            codigo_restricao=codigo_restricao,
            data_inicial=data_inicial,
            data_final=data_final,
            df=df,
        )

    def rhe_ls_lpp_earmi(
        self,
        codigo_restricao: Optional[int] = None,
        indice_reta: Optional[int] = None,
        coeficiente_angular: Optional[float] = None,
        coeficiente_linear: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroRHELsLPPEarmi, List[RegistroRHELsLPPEarmi], pd.DataFrame]
    ]:
        """
        Obtém um registro que cadastra as retas da restrição linear
        por partes de energia.

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param indice_reta: índice da reta definida
        :type indice_reta: int | None
        :param coeficiente_angular: coeficiente angular da reta
        :type coeficiente_angular: float | None
        :param coeficiente_linear: coeficiente linear da reta
        :type coeficiente_linear: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHELsLPPEarmi` |
            list[:class:`RegistroRHELsLPPEarmi`] | `pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroRHELsLPPEarmi,
            codigo_restricao=codigo_restricao,
            indice_reta=indice_reta,
            coeficiente_angular=coeficiente_angular,
            coeficiente_linear=coeficiente_linear,
            df=df,
        )

    def rhq(
        self,
        codigo_restricao: Optional[int] = None,
        formula: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[RegistroRHQ, List[RegistroRHQ], pd.DataFrame]]:
        """
        Obtém um registro que cadastra uma usina restrição de vazão (UHE).

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param formula: equação da restrição
        :type formula: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHQ` |
            list[:class:`RegistroRHQ`] | `pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroRHQ,
            codigo_restricao=codigo_restricao,
            formula=formula,
            df=df,
        )

    def rhq_horiz_per(
        self,
        codigo_restricao: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroRHQHorizPer, List[RegistroRHQHorizPer], pd.DataFrame]
    ]:
        """
        Obtém um registro que cadastra o horizonte de validade de uma
        restrição de vazão.

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param data_inicial: data inicial de validade da restrição
        :type data_inicial: datetime | None
        :param data_final: data final de validade da restrição
        :type data_final: datetime | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHQHorizPer` |
            list[:class:`RegistroRHQHorizPer`] | `pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroRHQHorizPer,
            codigo_restricao=codigo_restricao,
            data_inicial=data_inicial,
            data_final=data_final,
            df=df,
        )

    def rhq_ls_lpp_voli(
        self,
        codigo_restricao: Optional[int] = None,
        indice_reta: Optional[int] = None,
        coeficiente_angular: Optional[float] = None,
        coeficiente_linear: Optional[float] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroRHQLsLPPVoli, List[RegistroRHQLsLPPVoli], pd.DataFrame]
    ]:
        """
        Obtém um registro que cadastra as retas da restrição linear
        por partes de vazão.

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param indice_reta: índice da reta definida
        :type indice_reta: int | None
        :param coeficiente_angular: coeficiente angular da reta
        :type coeficiente_angular: float | None
        :param coeficiente_linear: coeficiente linear da reta
        :type coeficiente_linear: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHQLsLPPVoli` |
            list[:class:`RegistroRHQLsLPPVoli`] | `pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroRHQLsLPPVoli,
            codigo_restricao=codigo_restricao,
            indice_reta=indice_reta,
            coeficiente_angular=coeficiente_angular,
            coeficiente_linear=coeficiente_linear,
            df=df,
        )

    def rhq_lim_form_per_pat(
        self,
        codigo_restricao: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        patamar: Optional[int] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroRHQLimFormPerPat,
            List[RegistroRHQLimFormPerPat],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que cadastra as retas da restrição de vazão.

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param data_inicial: data de início da validade dos limites
        :type data_inicial: datetime | None
        :param data_final: data de fim da validade dos limites
        :type data_final: datetime | None
        :param patamar: patamar de validade dos limites
        :type patamar: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHQLimFormPerPat` |
            list[:class:`RegistroRHQLimFormPerPat`] | `pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroRHQLimFormPerPat,
            codigo_restricao=codigo_restricao,
            data_inicial=data_inicial,
            data_final=data_final,
            patamar=patamar,
            df=df,
        )

    def rhv(
        self,
        codigo_restricao: Optional[int] = None,
        formula: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[RegistroRHV, List[RegistroRHV], pd.DataFrame]]:
        """
        Obtém um registro que cadastra uma usina restrição de volume (UHE).

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param formula: equação da restrição
        :type formula: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHV` |
            list[:class:`RegistroRHV`] | `pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroRHV,
            codigo_restricao=codigo_restricao,
            formula=formula,
            df=df,
        )

    def rhv_horiz_per(
        self,
        codigo_restricao: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        df: bool = False,
    ) -> Optional[
        Union[RegistroRHVHorizPer, List[RegistroRHVHorizPer], pd.DataFrame]
    ]:
        """
        Obtém um registro que cadastra o horizonte de validade de uma
        restrição de volume.

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param data_inicial: data inicial de validade da restrição
        :type data_inicial: datetime | None
        :param data_final: data final de validade da restrição
        :type data_final: datetime | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHVHorizPer` |
            list[:class:`RegistroRHVHorizPer`] | `pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroRHVHorizPer,
            codigo_restricao=codigo_restricao,
            data_inicial=data_inicial,
            data_final=data_final,
            df=df,
        )

    def rhv_lim_form_per_pat(
        self,
        codigo_restricao: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        df: bool = False,
    ) -> Optional[
        Union[
            RegistroRHVLimFormPerPat,
            List[RegistroRHVLimFormPerPat],
            pd.DataFrame,
        ]
    ]:
        """
        Obtém um registro que cadastra as retas da restrição de volume.

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param data_inicial: data de início da validade dos limites
        :type data_inicial: datetime | None
        :param data_final: data de fim da validade dos limites
        :type data_final: datetime | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHVLimFormPerPat` |
            list[:class:`RegistroRHVLimFormPerPat`] | `pd.DataFrame` | None
        """
        return self.__registros_ou_df(
            RegistroRHVLimFormPerPat,
            codigo_restricao=codigo_restricao,
            data_inicial=data_inicial,
            data_final=data_final,
            df=df,
        )
