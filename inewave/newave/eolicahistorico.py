from typing import TypeVar, List, Optional, Union
from datetime import datetime

from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.eolicahistorico import (
    RegistroEolicaHistoricoVentoHorizonte,
    RegistroEolicaHistoricoVento,
    RegistroHistoricoVentoHorizonte,
    RegistroHistoricoVento,
)


class EolicaHistorico(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao histórico
    de ventos das usinas eólicas.
    """

    T = TypeVar("T")

    REGISTERS = [
        RegistroEolicaHistoricoVentoHorizonte,
        RegistroEolicaHistoricoVento,
        RegistroHistoricoVentoHorizonte,
        RegistroHistoricoVento,
    ]

    def eolica_historico_vento_horizonte(
        self,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
    ) -> Optional[
        Union[
            RegistroEolicaHistoricoVentoHorizonte,
            List[RegistroEolicaHistoricoVentoHorizonte],
        ]
    ]:
        """
        Obtém um registro que contém o horizonte de um histórico.

        :param data_inicial: data de início do histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do histórico
        :type data_final: datetime | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaHistoricoVentoHorizonte` |
            list[:class:`RegistroEolicaHistoricoVentoHorizonte`] | None
        """
        return self.data.get_registers_of_type(
            RegistroEolicaHistoricoVentoHorizonte,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def eolica_historico_vento(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        velocidade: Optional[float] = None,
        direcao: Optional[float] = None,
    ) -> Optional[
        Union[
            RegistroEolicaHistoricoVento,
            List[RegistroEolicaHistoricoVento],
        ]
    ]:
        """
        Obtém um registro que contém a o valor de vento para um
        intervalo do histórico.

        :param codigo_eolica: código da usina eólica
        :type codigo_eolica: int | None
        :param data_inicial: data de início do registro histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do registro histórico
        :type data_final: datetime | None
        :param velocidade: velocidade do vento
        :type velocidade: float | None
        :param direcao: direção do vento
        :type direcao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaHistoricoVento` |
            list[:class:`RegistroEolicaHistoricoVento`] | None
        """
        return self.data.get_registers_of_type(
            RegistroEolicaHistoricoVento,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            velocidade=velocidade,
            direcao=direcao,
        )

    def vento_hist_horiz(
        self,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
    ) -> Optional[
        Union[
            RegistroHistoricoVentoHorizonte,
            List[RegistroHistoricoVentoHorizonte],
        ]
    ]:
        """
        Obtém um registro que contém o horizonte de um histórico.

        :param data_inicial: data de início do histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do histórico
        :type data_final: datetime | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroHistoricoVentoHorizonte` |
            list[:class:`RegistroHistoricoVentoHorizonte`] | None
        """
        return self.data.get_registers_of_type(
            RegistroHistoricoVentoHorizonte,
            data_inicial=data_inicial,
            data_final=data_final,
        )

    def vento_hist(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        velocidade: Optional[float] = None,
        direcao: Optional[float] = None,
    ) -> Optional[
        Union[
            RegistroHistoricoVento,
            List[RegistroHistoricoVento],
        ]
    ]:
        """
        Obtém um registro que contém a o valor de vento para um
        intervalo do histórico.

        :param codigo_eolica: código da usina eólica
        :type codigo_eolica: int | None
        :param data_inicial: data de início do registro histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do registro histórico
        :type data_final: datetime | None
        :param velocidade: velocidade do vento
        :type velocidade: float | None
        :param direcao: direção do vento
        :type direcao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroHistoricoVento` |
            list[:class:`RegistroHistoricoVento`] | None
        """
        return self.data.get_registers_of_type(
            RegistroHistoricoVento,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            velocidade=velocidade,
            direcao=direcao,
        )
