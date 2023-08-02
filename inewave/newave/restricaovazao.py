from typing import TypeVar, List, Optional, Union
from datetime import datetime

from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.restricaovazao import (
    RegistroRHQ,
    RegistroRHQHorizPer,
    RegistroRHQLsLPPVoli,
)


class RestricaoVazao(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao cadastro
    das restrições lineares por partes no domínio de vazão (RHQ).
    """

    T = TypeVar("T")

    REGISTERS = [
        RegistroRHQLsLPPVoli,
        RegistroRHQHorizPer,
        RegistroRHQ,
    ]

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
        return self.data.get_registers_of_type(
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
        return self.data.get_registers_of_type(
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
        return self.data.get_registers_of_type(
            RegistroRHQLsLPPVoli,
            codigo_restricao=codigo_restricao,
            indice_reta=indice_reta,
            coeficiente_angular=coeficiente_angular,
            coeficiente_linear=coeficiente_linear,
        )
