from typing import TypeVar, List, Optional, Union
from datetime import datetime

from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.eolicaposto import (
    RegistroPEEPostoVento,
    RegistroPostoVentoCadastro,
)


class EolicaPosto(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos postos
    de vento e sua associação com os PEE.
    """

    T = TypeVar("T")

    REGISTERS = [
        RegistroPEEPostoVento,
        RegistroPostoVentoCadastro,
    ]

    def posto_vento_cad(
        self,
        codigo_posto: Optional[int] = None,
        nome_posto: Optional[str] = None,
    ) -> Optional[
        Union[
            RegistroPostoVentoCadastro,
            List[RegistroPostoVentoCadastro],
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
        return self.data.get_registers_of_type(
            RegistroPostoVentoCadastro,
            codigo_posto=codigo_posto,
            nome_posto=nome_posto,
        )

    def pee_posto(
        self,
        codigo_pee: Optional[datetime] = None,
        codigo_posto: Optional[datetime] = None,
    ) -> Optional[Union[RegistroPEEPostoVento, List[RegistroPEEPostoVento]]]:
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
        return self.data.get_registers_of_type(
            RegistroPEEPostoVento,
            codigo_pee=codigo_pee,
            codigo_posto=codigo_posto,
        )
