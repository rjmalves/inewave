from typing import TypeVar, List, Optional, Union

from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.eolicasubmercado import (
    RegistroEolicaSubmercado,
    RegistroPEESubmercado,
)


class EolicaSubmercado(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao mapeamento
    de usinas eólicas e submercados.
    """

    T = TypeVar("T")

    REGISTERS = [RegistroEolicaSubmercado, RegistroPEESubmercado]

    def eolica_submercado(
        self,
        codigo_eolica: Optional[int] = None,
        codigo_submercado: Optional[int] = None,
    ) -> Optional[
        Union[
            RegistroEolicaSubmercado,
            List[RegistroEolicaSubmercado],
        ]
    ]:
        """
        Obtém um registro que contém o mapeamento usina-submercado.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: int | None
        :param codigo_submercado: código que especifica o submercado
        :type codigo_submercado: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaSubmercado` |
            list[:class:`RegistroEolicaSubmercado`] | None
        """
        return self.data.get_registers_of_type(
            RegistroEolicaSubmercado,
            codigo_eolica=codigo_eolica,
            codigo_submercado=codigo_submercado,
        )

    def pee_subm(
        self,
        codigo_pee: Optional[int] = None,
        codigo_submercado: Optional[int] = None,
    ) -> Optional[Union[RegistroPEESubmercado, List[RegistroPEESubmercado]]]:
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
        return self.data.get_registers_of_type(
            RegistroPEESubmercado,
            codigo_pee=codigo_pee,
            codigo_submercado=codigo_submercado,
        )
