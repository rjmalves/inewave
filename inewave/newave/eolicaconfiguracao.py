from typing import TypeVar, List, Optional, Union
from datetime import datetime

from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.eolicaconfiguracao import (
    RegistroEolicaConfiguracao,
    RegistroPEEConfiguracaoPeriodo,
)


class EolicaConfiguracao(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às configurações
    das usinas eólicas.
    """

    T = TypeVar("T")

    REGISTERS = [RegistroEolicaConfiguracao, RegistroPEEConfiguracaoPeriodo]

    def eolica_configuracao(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        estado_operacao: Optional[str] = None,
    ) -> Optional[
        Union[
            RegistroEolicaConfiguracao,
            List[RegistroEolicaConfiguracao],
        ]
    ]:
        """
        Obtém um registro que contém a configuração de operação para
        uma usina eólica em um período.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: int | None
        :param data_inicial: período de início da configuração
        :type data_inicial: datetime | None
        :param data_final: período de fim da configuração
        :type data_final: datetime | None
        :param estado_operacao: tipo de operação
        :type estado_operacao: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaConfiguracao` |
            list[:class:`RegistroEolicaConfiguracao`] | None
        """
        return self.data.get_registers_of_type(
            RegistroEolicaConfiguracao,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            estado_operacao=estado_operacao,
        )

    def pee_config_per(
        self,
        codigo_pee: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        estado_operacao: Optional[str] = None,
    ) -> Optional[
        Union[
            RegistroPEEConfiguracaoPeriodo,
            List[RegistroPEEConfiguracaoPeriodo],
        ]
    ]:
        """
        Obtém um registro que contém a configuração de operação para
        um PEE em um período.

        :param codigo_pee: código que especifica o PEE
        :type codigo_pee: int | None
        :param data_inicial: período de início da configuração
        :type data_inicial: datetime | None
        :param data_final: período de fim da configuração
        :type data_final: datetime | None
        :param estado_operacao: tipo de operação
        :type estado_operacao: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEEConfiguracaoPeriodo` |
            list[:class:`RegistroPEEConfiguracaoPeriodo`] | None
        """
        return self.data.get_registers_of_type(
            RegistroPEEConfiguracaoPeriodo,
            codigo_pee=codigo_pee,
            data_inicial=data_inicial,
            data_final=data_final,
            estado_operacao=estado_operacao,
        )
