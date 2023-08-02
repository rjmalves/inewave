from typing import TypeVar, List, Optional, Union
from datetime import datetime

from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.eolicageracao import (
    RegistroEolicaGeracaoPeriodo,
    RegistroEolicaGeracaoPatamar,
    RegistroPEEGeracaoPatamar,
)


class EolicaGeracao(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao histórico
    de geração das usinas eólicas.
    """

    T = TypeVar("T")

    REGISTERS = [
        RegistroEolicaGeracaoPeriodo,
        RegistroEolicaGeracaoPatamar,
        RegistroPEEGeracaoPatamar,
    ]

    def eolica_geracao_periodo(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        geracao: Optional[float] = None,
    ) -> Optional[
        Union[
            RegistroEolicaGeracaoPeriodo,
            List[RegistroEolicaGeracaoPeriodo],
        ]
    ]:
        """
        Obtém um registro que contém o valor de geração para uma usina
        eólica durante um período.

        :param codigo_eolica: código da usina eólica
        :type codigo_eolica: int | None
        :param data_inicial: data de início do histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do histórico
        :type data_final: datetime | None
        :param geracao: valor de geração
        :type geracao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaGeracaoPeriodo` |
            list[:class:`RegistroEolicaGeracaoPeriodo`] | None
        """
        return self.data.get_registers_of_type(
            RegistroEolicaGeracaoPeriodo,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            geracao=geracao,
        )

    def eolica_geracao_profundidade_periodo_patamar(
        self,
        codigo_eolica: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        indice_patamar: Optional[int] = None,
        profundidade: Optional[float] = None,
    ) -> Optional[
        Union[
            RegistroEolicaGeracaoPatamar,
            List[RegistroEolicaGeracaoPatamar],
        ]
    ]:
        """
        Obtém um registro que contém a profundidade de um patamar
        de geração para um período.

        :param codigo_eolica: código da usina eólica
        :type codigo_eolica: int | None
        :param data_inicial: data de início do registro histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do registro histórico
        :type data_final: datetime | None
        :param indice_patamar: patamar de geração eólica
        :type indice_patamar: int | None
        :param profundidade: profundidade do patamar de geração
        :type profundidade: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaGeracaoPatamar` |
            list[:class:`RegistroEolicaGeracaoPatamar`] | None
        """
        return self.data.get_registers_of_type(
            RegistroEolicaGeracaoPatamar,
            codigo_eolica=codigo_eolica,
            data_inicial=data_inicial,
            data_final=data_final,
            indice_patamar=indice_patamar,
            profundidade=profundidade,
        )

    def pee_ger_prof_per_pat(
        self,
        codigo_pee: Optional[int] = None,
        data_inicial: Optional[datetime] = None,
        data_final: Optional[datetime] = None,
        indice_patamar: Optional[int] = None,
        profundidade: Optional[float] = None,
    ) -> Optional[
        Union[
            RegistroPEEGeracaoPatamar,
            List[RegistroPEEGeracaoPatamar],
        ]
    ]:
        """
        Obtém um registro que contém a profundidade de um patamar
        de geração para um período, para um PEE.

        :param codigo_pee: código do PEE
        :type codigo_pee: int | None
        :param data_inicial: data de início do registro histórico
        :type data_inicial: datetime | None
        :param data_final: data de fim do registro histórico
        :type data_final: datetime | None
        :param indice_patamar: patamar de geração eólica
        :type indice_patamar: int | None
        :param profundidade: profundidade do patamar de geração
        :type profundidade: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroPEEGeracaoPatamar` |
            list[:class:`RegistroPEEGeracaoPatamar`] | None
        """
        return self.data.get_registers_of_type(
            RegistroPEEGeracaoPatamar,
            codigo_pee=codigo_pee,
            data_inicial=data_inicial,
            data_final=data_final,
            indice_patamar=indice_patamar,
            profundidade=profundidade,
        )
