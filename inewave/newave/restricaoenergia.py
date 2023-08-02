from typing import TypeVar, List, Optional, Union
from datetime import datetime

from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.restricaoenergia import (
    RegistroRHE,
    RegistroRHEHorizPer,
    RegistroRHELsLPPEarmi,
)


class RestricaoEnergia(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao cadastro
    das restrições lineares por partes no domínio de energia (REE).
    """

    T = TypeVar("T")

    REGISTERS = [
        RegistroRHELsLPPEarmi,
        RegistroRHEHorizPer,
        RegistroRHE,
    ]

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
        return self.data.get_registers_of_type(
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
        return self.data.get_registers_of_type(
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
        return self.data.get_registers_of_type(
            RegistroRHELsLPPEarmi,
            codigo_restricao=codigo_restricao,
            indice_reta=indice_reta,
            coeficiente_angular=coeficiente_angular,
            coeficiente_linear=coeficiente_linear,
        )
