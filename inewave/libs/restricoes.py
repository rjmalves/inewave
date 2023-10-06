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
        RegistroRHQLsLPPVoli,
        RegistroRHQHorizPer,
        RegistroRHQ,
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
    ) -> Optional[Union[RegistroRE, List[RegistroRE]]]:
        """
        Obtém um registro que cadastra uma usina restrição elétrica (RE).

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param formula: equação da restrição
        :type formula: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRE` |
            list[:class:`RegistroRE`] | None
        """
        return self.__registros_ou_df(
            RegistroRE,
            codigo_restricao=codigo_restricao,
            formula=formula,
        )

    def re_horiz_per(
        self,
        codigo_restricao: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
    ) -> Optional[Union[RegistroREHorizPer, List[RegistroREHorizPer]]]:
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
            list[:class:`RegistroREHorizPer`] | None
        """
        return self.__registros_ou_df(
            RegistroREHorizPer,
            codigo_restricao=codigo_restricao,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def re_lim_form_per(
        self,
        codigo_restricao: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        patamar: Optional[int] = None,
        limite_inferior: Optional[float] = None,
        limite_superior: Optional[float] = None,
    ) -> Optional[Union[RegistroRELimFormPer, List[RegistroRELimFormPer]]]:
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
            list[:class:`RegistroRELimFormPer`] | None
        """
        return self.__registros_ou_df(
            RegistroRELimFormPer,
            codigo_restricao=codigo_restricao,
            data_inicial=data_inicial,
            data_final=data_final,
            patamar=patamar,
            limite_inferior=limite_inferior,
            limite_superior=limite_superior,
        )

    def rhe(
        self,
        codigo_restricao: Optional[int] = None,
        formula: Optional[str] = None,
    ) -> Optional[Union[RegistroRHE, List[RegistroRHE]]]:
        """
        Obtém um registro que cadastra uma usina restrição linear por
        partes de energia (REE).

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param formula: equação da restrição
        :type formula: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHE` |
            list[:class:`RegistroRHE`] | None
        """
        return self.__registros_ou_df(
            RegistroRHE,
            codigo_restricao=codigo_restricao,
            formula=formula,
        )

    def rhe_horiz_per(
        self,
        codigo_restricao: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
    ) -> Optional[Union[RegistroRHEHorizPer, List[RegistroRHEHorizPer]]]:
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
            list[:class:`RegistroRHEHorizPer`] | None
        """
        return self.__registros_ou_df(
            RegistroRHEHorizPer,
            codigo_restricao=codigo_restricao,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def rhe_ls_lpp_earmi(
        self,
        codigo_restricao: Optional[int] = None,
        indice_reta: Optional[int] = None,
        coeficiente_angular: Optional[float] = None,
        coeficiente_linear: Optional[float] = None,
    ) -> Optional[Union[RegistroRHELsLPPEarmi, List[RegistroRHELsLPPEarmi]]]:
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
            list[:class:`RegistroRHELsLPPEarmi`] | None
        """
        return self.__registros_ou_df(
            RegistroRHELsLPPEarmi,
            codigo_restricao=codigo_restricao,
            indice_reta=indice_reta,
            coeficiente_angular=coeficiente_angular,
            coeficiente_linear=coeficiente_linear,
        )

    def rhq(
        self,
        codigo_restricao: Optional[int] = None,
        formula: Optional[str] = None,
    ) -> Optional[Union[RegistroRHQ, List[RegistroRHQ]]]:
        """
        Obtém um registro que cadastra uma usina restrição linear por
        partes de vazão (UHE).

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param formula: equação da restrição
        :type formula: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHQ` |
            list[:class:`RegistroRHQ`] | None
        """
        return self.__registros_ou_df(
            RegistroRHQ,
            codigo_restricao=codigo_restricao,
            formula=formula,
        )

    def rhq_horiz_per(
        self,
        codigo_restricao: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
    ) -> Optional[Union[RegistroRHQHorizPer, List[RegistroRHQHorizPer]]]:
        """
        Obtém um registro que cadastra o horizonte de validade de uma
        restrição linear por partes de vazão.

        :param codigo_restricao: código que especifica a restrição
        :type codigo_restricao: int | None
        :param data_inicial: data inicial de validade da restrição
        :type data_inicial: datetime | None
        :param data_final: data final de validade da restrição
        :type data_final: datetime | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroRHQHorizPer` |
            list[:class:`RegistroRHQHorizPer`] | None
        """
        return self.__registros_ou_df(
            RegistroRHQHorizPer,
            codigo_restricao=codigo_restricao,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def rhq_ls_lpp_voli(
        self,
        codigo_restricao: Optional[int] = None,
        indice_reta: Optional[int] = None,
        coeficiente_angular: Optional[float] = None,
        coeficiente_linear: Optional[float] = None,
    ) -> Optional[Union[RegistroRHQLsLPPVoli, List[RegistroRHQLsLPPVoli]]]:
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
            list[:class:`RegistroRHQLsLPPVoli`] | None
        """
        return self.__registros_ou_df(
            RegistroRHQLsLPPVoli,
            codigo_restricao=codigo_restricao,
            indice_reta=indice_reta,
            coeficiente_angular=coeficiente_angular,
            coeficiente_linear=coeficiente_linear,
        )
