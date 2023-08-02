from typing import TypeVar, List, Optional, Union
from datetime import datetime

from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.restricaoeletrica import (
    RegistroRE,
    RegistroREHorizPer,
    RegistroRELimFormPer,
)


class RestricaoEletrica(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao cadastro
    das restrições lineares por partes no domínio de energia (REE).
    """

    T = TypeVar("T")

    REGISTERS = [
        RegistroRELimFormPer,
        RegistroREHorizPer,
        RegistroRE,
    ]

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
        return self.data.get_registers_of_type(
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
        return self.data.get_registers_of_type(
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
        return self.data.get_registers_of_type(
            RegistroRELimFormPer,
            codigo_restricao=codigo_restricao,
            data_inicial=data_inicial,
            data_final=data_final,
            patamar=patamar,
            limite_inferior=limite_inferior,
            limite_superior=limite_superior,
        )
