from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.modif import (
    USINA,
    VOLMIN,
    VOLMAX,
    NUMCNJ,
    NUMMAQ,
    VAZMIN,
    CFUGA,
    CMONT,
    VMAXT,
    VMINT,
    VMINP,
    VAZMINT,
    VAZMAXT,
    TURBMAXT,
    TURBMINT,
)

from datetime import datetime
from typing import TypeVar, List, Optional, Union
import pandas as pd  # type: ignore


class Modif(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às alterações nas
    configurações das usinas hidroelétricas.
    """

    T = TypeVar("T")

    REGISTERS = [
        USINA,
        VOLMIN,
        VOLMAX,
        NUMCNJ,
        NUMMAQ,
        VAZMIN,
        CFUGA,
        CMONT,
        VMAXT,
        VMINT,
        VMINP,
        VAZMINT,
        VAZMAXT,
        TURBMAXT,
        TURBMINT,
    ]

    def usina(
        self,
        codigo: Optional[int] = None,
        nome: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[USINA, List[USINA], pd.DataFrame]]:
        """
        Obtém um registro que define a usina modificada.

        :param codigo: código da usina modificada
        :type codigo: int | None
        :param nome: nome da usina
        :type nome: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`USINA` | list[:class:`USINA`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(
                USINA, codigo=codigo, nome=nome
            )

    def volmin(
        self,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[VOLMIN, List[VOLMIN], pd.DataFrame]]:
        """
        Obtém um registro que define um volume mínimo.

        :param volume: volume mínimo
        :type volume: float | None
        :param unidade: unidade do volume
        :type unidade: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VOLMIN` | list[:class:`VOLMIN`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(
                VOLMIN, volume=volume, unidade=unidade
            )

    def volmax(
        self,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[VOLMAX, List[VOLMAX], pd.DataFrame]]:
        """
        Obtém um registro que define um volume máximo.

        :param volume: volume máximo
        :type volume: float | None
        :param unidade: unidade do volume
        :type unidade: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VOLMAX` | list[:class:`VOLMAX`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(
                VOLMAX, volume=volume, unidade=unidade
            )

    def numcnj(
        self,
        numero: Optional[int] = None,
        df: bool = False,
    ) -> Optional[Union[NUMCNJ, List[NUMCNJ], pd.DataFrame]]:
        """
        Obtém um registro que um número de conjuntos de máquinas.

        :param numero: o número
        :type numero: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`NUMCNJ` | list[:class:`NUMCNJ`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(NUMCNJ, numero=numero)

    def nummaq(
        self,
        conjunto: Optional[int] = None,
        numero_maquinas: Optional[int] = None,
        df: bool = False,
    ) -> Optional[Union[NUMMAQ, List[NUMMAQ], pd.DataFrame]]:
        """
        Obtém um registro que um número de máquinas por
            conjunto de máquinas.

        :param conjunto: o conjunto
        :type conjunto: int | None
        :param numero_maquinas: o número de máquinas
        :type numero_maquinas: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`NUMMAQ` | list[:class:`NUMMAQ`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(
                NUMMAQ, conjunto=conjunto, numero_maquinas=numero_maquinas
            )

    def vazmin(
        self,
        vazao: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[VAZMIN, List[VAZMIN], pd.DataFrame]]:
        """
        Obtém um registro que define uma vazão mínima.

        :param vazao: vazão mínima
        :type vazao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VAZMIN` | list[:class:`VAZMIN`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(VAZMIN, vazao=vazao)

    def cfuga(
        self,
        data_inicio: Optional[datetime] = None,
        nivel: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[CFUGA, List[CFUGA], pd.DataFrame]]:
        """
        Obtém um registro que define o nível do canal de fuga.

        :param data_inicio: data de início da validade do nível
        :type data_inicio: datetime | None
        :param nivel: o nível
        :type nivel: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`CFUGA` | list[:class:`CFUGA`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(
                CFUGA, data_inicio=data_inicio, nivel=nivel
            )

    def cmont(
        self,
        data_inicio: Optional[datetime] = None,
        nivel: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[CMONT, List[CMONT], pd.DataFrame]]:
        """
        Obtém um registro que define o nível do canal de montante.

        :param data_inicio: data de início da validade do nível
        :type data_inicio: datetime | None
        :param nivel: o nível
        :type nivel: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`CMONT` | list[:class:`CMONT`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(
                CMONT, data_inicio=data_inicio, nivel=nivel
            )

    def vmaxt(
        self,
        data_inicio: Optional[datetime] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[VMAXT, List[VMAXT], pd.DataFrame]]:
        """
        Obtém um registro que define o volume máximo por período.

        :param data_inicio: data de início da validade do volume
        :type data_inicio: datetime | None
        :param volume: o volume
        :type volume: float | None
        :param unidade: a unidade do volume
        :type unidade: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VMAXT` | list[:class:`VMAXT`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(
                VMAXT, data_inicio=data_inicio, volume=volume, unidade=unidade
            )

    def vmint(
        self,
        data_inicio: Optional[datetime] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[VMINT, List[VMINT], pd.DataFrame]]:
        """
        Obtém um registro que define o volume mínimo por período.

        :param data_inicio: data de início da validade do volume
        :type data_inicio: datetime | None
        :param volume: o volume
        :type volume: float | None
        :param unidade: a unidade do volume
        :type unidade: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VMINT` | list[:class:`VMINT`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(
                VMINT, data_inicio=data_inicio, volume=volume, unidade=unidade
            )

    def vminp(
        self,
        data_inicio: Optional[datetime] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[VMINP, List[VMINP], pd.DataFrame]]:
        """
        Obtém um registro que define o volume mínimo para penalidade.

        :param data_inicio: data de início da validade do volume
        :type data_inicio: datetime | None
        :param volume: o volume
        :type volume: float | None
        :param unidade: a unidade do volume
        :type unidade: str | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VMINP` | list[:class:`VMINP`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(
                VMINP, data_inicio=data_inicio, volume=volume, unidade=unidade
            )

    def vazmint(
        self,
        data_inicio: Optional[datetime] = None,
        vazao: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[VAZMINT, List[VAZMINT], pd.DataFrame]]:
        """
        Obtém um registro que define a vazão mínima por período.

        :param data_inicio: data de início da validade do volume
        :type data_inicio: datetime | None
        :param vazao: a vazão mínima
        :type vazao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VAZMINT` | list[:class:`VAZMINT`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(
                VAZMINT, data_inicio=data_inicio, vazao=vazao
            )

    def vazmaxt(
        self,
        data_inicio: Optional[datetime] = None,
        vazao: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[VAZMAXT, List[VAZMAXT], pd.DataFrame]]:
        """
        Obtém um registro que define a vazão máxima por período.

        :param data_inicio: data de início da validade do volume
        :type data_inicio: datetime | None
        :param vazao: a vazão máxima
        :type vazao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VAZMAXT` | list[:class:`VAZMAXT`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(
                VAZMAXT, data_inicio=data_inicio, vazao=vazao
            )

    def turbmaxt(
        self,
        data_inicio: Optional[datetime] = None,
        turbinamento: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[TURBMAXT, List[TURBMAXT], pd.DataFrame]]:
        """
        Obtém um registro que define o turbinamento máximo por período.

        :param data_inicio: data de início da validade do turbinamento
        :type data_inicio: datetime | None
        :param turbinamento: o turbinamento máximo
        :type turbinamento: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`TURBMAXT` | list[:class:`TURBMAXT`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(
                TURBMAXT, data_inicio=data_inicio, turbinamento=turbinamento
            )

    def turbmint(
        self,
        data_inicio: Optional[datetime] = None,
        turbinamento: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[TURBMINT, List[TURBMINT], pd.DataFrame]]:
        """
        Obtém um registro que define o turbinamento mínimo por período.

        :param data_inicio: data de início da validade do turbinamento
        :type data_inicio: datetime | None
        :param turbinamento: o turbinamento mínimo
        :type turbinamento: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`TURBMINT` | list[:class:`TURBMINT`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(USINA)
        else:
            return self.data.get_registers_of_type(
                TURBMINT, data_inicio=data_inicio, turbinamento=turbinamento
            )

    def modificacoes_usina(self, codigo: int) -> Optional[List[Register]]:
        """
        Filtra os registros que são associados a uma usina específica.

        :param codigo: O código da usina
        :type codigo: int
        :return: Os registros que modificam a usina
        :rtype: List[Register]
        """
        usinas = self.usina()
        if usinas is None or isinstance(usinas, USINA):
            return None
        reg_usina: List[USINA] = list(
            filter(lambda r: r.codigo == codigo, usinas)
        )
        modificacoes_usina: List[Register] = []
        if len(reg_usina) > 0:
            r = reg_usina[0].next
            while not (isinstance(r, USINA) or r.is_last):
                modificacoes_usina.append(r)
                r = r.next

        return modificacoes_usina
