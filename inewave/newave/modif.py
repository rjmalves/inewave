from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.modif import (
    USINA,
    VOLMIN,
    VOLMAX,
    NUMCNJ,
    NUMMAQ,
    POTEFE,
    PRODESP,
    TEIF,
    IP,
    PERDHIDR,
    VOLCOTA,
    COTAREA,
    VAZMIN,
    COEFEVAP,
    CFUGA,
    CMONT,
    VMAXT,
    VMINT,
    NUMBAS,
    VMINP,
    VAZMINT,
    VAZMAXT,
    TURBMAXT,
    TURBMINT,
    CDESVIO,
)

from datetime import datetime
from typing import TypeVar, List, Optional, Union, Literal, overload
import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package


class Modif(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às alterações nas
    configurações das usinas hidroelétricas.
    """

    __slots__: List[str] = []

    T = TypeVar("T")

    REGISTERS = [
        USINA,
        VOLMIN,
        VOLMAX,
        NUMCNJ,
        NUMMAQ,
        POTEFE,
        PRODESP,
        TEIF,
        IP,
        PERDHIDR,
        VOLCOTA,
        COTAREA,
        VAZMIN,
        COEFEVAP,
        CFUGA,
        CMONT,
        VMAXT,
        VMINT,
        NUMBAS,
        VMINP,
        VAZMINT,
        VAZMAXT,
        TURBMAXT,
        TURBMINT,
        CDESVIO,
    ]

    @overload
    def usina(
        self,
        codigo: Optional[int] = None,
        nome: Optional[str] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def usina(
        self,
        codigo: Optional[int] = None,
        nome: Optional[str] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[USINA, List[USINA]]]: ...
    @overload
    def usina(
        self,
        codigo: Optional[int] = None,
        nome: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[USINA, List[USINA], pd.DataFrame]]: ...
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

    @overload
    def volmin(
        self,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def volmin(
        self,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[VOLMIN, List[VOLMIN]]]: ...
    @overload
    def volmin(
        self,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[VOLMIN, List[VOLMIN], pd.DataFrame]]: ...
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
            return self._as_df(VOLMIN)
        else:
            return self.data.get_registers_of_type(
                VOLMIN, volume=volume, unidade=unidade
            )

    @overload
    def volmax(
        self,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def volmax(
        self,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[VOLMAX, List[VOLMAX]]]: ...
    @overload
    def volmax(
        self,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[VOLMAX, List[VOLMAX], pd.DataFrame]]: ...
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
            return self._as_df(VOLMAX)
        else:
            return self.data.get_registers_of_type(
                VOLMAX, volume=volume, unidade=unidade
            )

    @overload
    def numcnj(
        self, numero: Optional[int] = None, *, df: Literal[True]
    ) -> pd.DataFrame: ...
    @overload
    def numcnj(
        self, numero: Optional[int] = None, df: Literal[False] = False
    ) -> Optional[Union[NUMCNJ, List[NUMCNJ]]]: ...
    @overload
    def numcnj(
        self, numero: Optional[int] = None, df: bool = False
    ) -> Optional[Union[NUMCNJ, List[NUMCNJ], pd.DataFrame]]: ...
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
            return self._as_df(NUMCNJ)
        else:
            return self.data.get_registers_of_type(NUMCNJ, numero=numero)

    @overload
    def nummaq(
        self,
        conjunto: Optional[int] = None,
        numero_maquinas: Optional[int] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def nummaq(
        self,
        conjunto: Optional[int] = None,
        numero_maquinas: Optional[int] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[NUMMAQ, List[NUMMAQ]]]: ...
    @overload
    def nummaq(
        self,
        conjunto: Optional[int] = None,
        numero_maquinas: Optional[int] = None,
        df: bool = False,
    ) -> Optional[Union[NUMMAQ, List[NUMMAQ], pd.DataFrame]]: ...
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
            return self._as_df(NUMMAQ)
        else:
            return self.data.get_registers_of_type(
                NUMMAQ, conjunto=conjunto, numero_maquinas=numero_maquinas
            )

    @overload
    def potefe(
        self,
        potencia: Optional[float] = None,
        conjunto: Optional[int] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def potefe(
        self,
        potencia: Optional[float] = None,
        conjunto: Optional[int] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[POTEFE, List[POTEFE]]]: ...
    @overload
    def potefe(
        self,
        potencia: Optional[float] = None,
        conjunto: Optional[int] = None,
        df: bool = False,
    ) -> Optional[Union[POTEFE, List[POTEFE], pd.DataFrame]]: ...
    def potefe(
        self,
        potencia: Optional[float] = None,
        conjunto: Optional[int] = None,
        df: bool = False,
    ) -> Optional[Union[POTEFE, List[POTEFE], pd.DataFrame]]:
        """
        Obtém um registro que define a potência efetiva de um
            conjunto de máquinas.

        :param potencia: a potência efetiva em MW
        :type potencia: float | None
        :param conjunto: o conjunto
        :type conjunto: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`POTEFE` | list[:class:`POTEFE`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(POTEFE)
        else:
            return self.data.get_registers_of_type(
                POTEFE, potencia=potencia, conjunto=conjunto
            )

    @overload
    def prodesp(
        self, produtibilidade: Optional[float] = None, *, df: Literal[True]
    ) -> pd.DataFrame: ...
    @overload
    def prodesp(
        self,
        produtibilidade: Optional[float] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[PRODESP, List[PRODESP]]]: ...
    @overload
    def prodesp(
        self, produtibilidade: Optional[float] = None, df: bool = False
    ) -> Optional[Union[PRODESP, List[PRODESP], pd.DataFrame]]: ...
    def prodesp(
        self,
        produtibilidade: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[PRODESP, List[PRODESP], pd.DataFrame]]:
        """
        Obtém um registro que define a produtibilidade específica.

        :param produtibilidade: a produtibilidade específica em MW/m3/s/m
        :type produtibilidade: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`PRODESP` | list[:class:`PRODESP`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(PRODESP)
        else:
            return self.data.get_registers_of_type(
                PRODESP, produtibilidade=produtibilidade
            )

    @overload
    def teif(
        self, teif: Optional[float] = None, *, df: Literal[True]
    ) -> pd.DataFrame: ...
    @overload
    def teif(
        self, teif: Optional[float] = None, df: Literal[False] = False
    ) -> Optional[Union[TEIF, List[TEIF]]]: ...
    @overload
    def teif(
        self, teif: Optional[float] = None, df: bool = False
    ) -> Optional[Union[TEIF, List[TEIF], pd.DataFrame]]: ...
    def teif(
        self,
        teif: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[TEIF, List[TEIF], pd.DataFrame]]:
        """
        Obtém um registro que define a taxa esperada de indisponibilidade
            forçada.

        :param teif: a taxa esperada de indisponibilidade forçada em %
        :type teif: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`TEIF` | list[:class:`TEIF`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(TEIF)
        else:
            return self.data.get_registers_of_type(TEIF, teif=teif)

    @overload
    def ip(
        self, ip: Optional[float] = None, *, df: Literal[True]
    ) -> pd.DataFrame: ...
    @overload
    def ip(
        self, ip: Optional[float] = None, df: Literal[False] = False
    ) -> Optional[Union[IP, List[IP]]]: ...
    @overload
    def ip(
        self, ip: Optional[float] = None, df: bool = False
    ) -> Optional[Union[IP, List[IP], pd.DataFrame]]: ...
    def ip(
        self,
        ip: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[IP, List[IP], pd.DataFrame]]:
        """
        Obtém um registro que define a indisponibilidade programada.

        :param ip: a indisponibilidade programada em %
        :type ip: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`IP` | list[:class:`IP`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(IP)
        else:
            return self.data.get_registers_of_type(IP, ip=ip)

    @overload
    def perdhidr(
        self, perdas: Optional[float] = None, *, df: Literal[True]
    ) -> pd.DataFrame: ...
    @overload
    def perdhidr(
        self, perdas: Optional[float] = None, df: Literal[False] = False
    ) -> Optional[Union[PERDHIDR, List[PERDHIDR]]]: ...
    @overload
    def perdhidr(
        self, perdas: Optional[float] = None, df: bool = False
    ) -> Optional[Union[PERDHIDR, List[PERDHIDR], pd.DataFrame]]: ...
    def perdhidr(
        self,
        perdas: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[PERDHIDR, List[PERDHIDR], pd.DataFrame]]:
        """
        Obtém um registro que define a perda hidráulica.

        :param perdas: a perda hidráulica, na unidade do cadastro
        :type perdas: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`PERDHIDR` | list[:class:`PERDHIDR`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(PERDHIDR)
        else:
            return self.data.get_registers_of_type(PERDHIDR, perdas=perdas)

    @overload
    def volcota(
        self,
        polinomio_volume_cota: Optional[List[float]] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def volcota(
        self,
        polinomio_volume_cota: Optional[List[float]] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[VOLCOTA, List[VOLCOTA]]]: ...
    @overload
    def volcota(
        self,
        polinomio_volume_cota: Optional[List[float]] = None,
        df: bool = False,
    ) -> Optional[Union[VOLCOTA, List[VOLCOTA], pd.DataFrame]]: ...
    def volcota(
        self,
        polinomio_volume_cota: Optional[List[float]] = None,
        df: bool = False,
    ) -> Optional[Union[VOLCOTA, List[VOLCOTA], pd.DataFrame]]:
        """
        Obtém um registro que define o polinômio volume-cota.

        :param polinomio_volume_cota: os coeficientes a0 a a4
        :type polinomio_volume_cota: list[float] | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`VOLCOTA` | list[:class:`VOLCOTA`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(VOLCOTA)
        else:
            return self.data.get_registers_of_type(
                VOLCOTA, polinomio_volume_cota=polinomio_volume_cota
            )

    @overload
    def cotarea(
        self,
        polinomio_cota_area: Optional[List[float]] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def cotarea(
        self,
        polinomio_cota_area: Optional[List[float]] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[COTAREA, List[COTAREA]]]: ...
    @overload
    def cotarea(
        self,
        polinomio_cota_area: Optional[List[float]] = None,
        df: bool = False,
    ) -> Optional[Union[COTAREA, List[COTAREA], pd.DataFrame]]: ...
    def cotarea(
        self,
        polinomio_cota_area: Optional[List[float]] = None,
        df: bool = False,
    ) -> Optional[Union[COTAREA, List[COTAREA], pd.DataFrame]]:
        """
        Obtém um registro que define o polinômio cota-área.

        :param polinomio_cota_area: os coeficientes a0 a a4
        :type polinomio_cota_area: list[float] | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`COTAREA` | list[:class:`COTAREA`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(COTAREA)
        else:
            return self.data.get_registers_of_type(
                COTAREA, polinomio_cota_area=polinomio_cota_area
            )

    @overload
    def vazmin(
        self, vazao: Optional[float] = None, *, df: Literal[True]
    ) -> pd.DataFrame: ...
    @overload
    def vazmin(
        self, vazao: Optional[float] = None, df: Literal[False] = False
    ) -> Optional[Union[VAZMIN, List[VAZMIN]]]: ...
    @overload
    def vazmin(
        self, vazao: Optional[float] = None, df: bool = False
    ) -> Optional[Union[VAZMIN, List[VAZMIN], pd.DataFrame]]: ...
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
            return self._as_df(VAZMIN)
        else:
            return self.data.get_registers_of_type(VAZMIN, vazao=vazao)

    @overload
    def coefevap(
        self,
        coeficiente: Optional[int] = None,
        mes: Optional[int] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def coefevap(
        self,
        coeficiente: Optional[int] = None,
        mes: Optional[int] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[COEFEVAP, List[COEFEVAP]]]: ...
    @overload
    def coefevap(
        self,
        coeficiente: Optional[int] = None,
        mes: Optional[int] = None,
        df: bool = False,
    ) -> Optional[Union[COEFEVAP, List[COEFEVAP], pd.DataFrame]]: ...
    def coefevap(
        self,
        coeficiente: Optional[int] = None,
        mes: Optional[int] = None,
        df: bool = False,
    ) -> Optional[Union[COEFEVAP, List[COEFEVAP], pd.DataFrame]]:
        """
        Obtém um registro que define o coeficiente de evaporação de um
            mês.

        :param coeficiente: o coeficiente de evaporação em mm/mês
        :type coeficiente: int | None
        :param mes: o mês do coeficiente (1 a 12)
        :type mes: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`COEFEVAP` | list[:class:`COEFEVAP`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(COEFEVAP)
        else:
            return self.data.get_registers_of_type(
                COEFEVAP, coeficiente=coeficiente, mes=mes
            )

    @overload
    def cfuga(
        self,
        data_inicio: Optional[datetime] = None,
        nivel: Optional[float] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def cfuga(
        self,
        data_inicio: Optional[datetime] = None,
        nivel: Optional[float] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[CFUGA, List[CFUGA]]]: ...
    @overload
    def cfuga(
        self,
        data_inicio: Optional[datetime] = None,
        nivel: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[CFUGA, List[CFUGA], pd.DataFrame]]: ...
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
            return self._as_df(CFUGA)
        else:
            return self.data.get_registers_of_type(
                CFUGA, data_inicio=data_inicio, nivel=nivel
            )

    @overload
    def cmont(
        self,
        data_inicio: Optional[datetime] = None,
        nivel: Optional[float] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def cmont(
        self,
        data_inicio: Optional[datetime] = None,
        nivel: Optional[float] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[CMONT, List[CMONT]]]: ...
    @overload
    def cmont(
        self,
        data_inicio: Optional[datetime] = None,
        nivel: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[CMONT, List[CMONT], pd.DataFrame]]: ...
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
            return self._as_df(CMONT)
        else:
            return self.data.get_registers_of_type(
                CMONT, data_inicio=data_inicio, nivel=nivel
            )

    @overload
    def vmaxt(
        self,
        data_inicio: Optional[datetime] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def vmaxt(
        self,
        data_inicio: Optional[datetime] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[VMAXT, List[VMAXT]]]: ...
    @overload
    def vmaxt(
        self,
        data_inicio: Optional[datetime] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[VMAXT, List[VMAXT], pd.DataFrame]]: ...
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
            return self._as_df(VMAXT)
        else:
            return self.data.get_registers_of_type(
                VMAXT, data_inicio=data_inicio, volume=volume, unidade=unidade
            )

    @overload
    def vmint(
        self,
        data_inicio: Optional[datetime] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def vmint(
        self,
        data_inicio: Optional[datetime] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[VMINT, List[VMINT]]]: ...
    @overload
    def vmint(
        self,
        data_inicio: Optional[datetime] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[VMINT, List[VMINT], pd.DataFrame]]: ...
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
            return self._as_df(VMINT)
        else:
            return self.data.get_registers_of_type(
                VMINT, data_inicio=data_inicio, volume=volume, unidade=unidade
            )

    @overload
    def numbas(
        self, numero: Optional[int] = None, *, df: Literal[True]
    ) -> pd.DataFrame: ...
    @overload
    def numbas(
        self, numero: Optional[int] = None, df: Literal[False] = False
    ) -> Optional[Union[NUMBAS, List[NUMBAS]]]: ...
    @overload
    def numbas(
        self, numero: Optional[int] = None, df: bool = False
    ) -> Optional[Union[NUMBAS, List[NUMBAS], pd.DataFrame]]: ...
    def numbas(
        self,
        numero: Optional[int] = None,
        df: bool = False,
    ) -> Optional[Union[NUMBAS, List[NUMBAS], pd.DataFrame]]:
        """
        Obtém um registro que define o número de unidades de base.

        :param numero: o número de unidades de base
        :type numero: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`NUMBAS` | list[:class:`NUMBAS`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(NUMBAS)
        else:
            return self.data.get_registers_of_type(NUMBAS, numero=numero)

    @overload
    def vminp(
        self,
        data_inicio: Optional[datetime] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def vminp(
        self,
        data_inicio: Optional[datetime] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[VMINP, List[VMINP]]]: ...
    @overload
    def vminp(
        self,
        data_inicio: Optional[datetime] = None,
        volume: Optional[float] = None,
        unidade: Optional[str] = None,
        df: bool = False,
    ) -> Optional[Union[VMINP, List[VMINP], pd.DataFrame]]: ...
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
            return self._as_df(VMINP)
        else:
            return self.data.get_registers_of_type(
                VMINP, data_inicio=data_inicio, volume=volume, unidade=unidade
            )

    @overload
    def vazmint(
        self,
        data_inicio: Optional[datetime] = None,
        vazao: Optional[float] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def vazmint(
        self,
        data_inicio: Optional[datetime] = None,
        vazao: Optional[float] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[VAZMINT, List[VAZMINT]]]: ...
    @overload
    def vazmint(
        self,
        data_inicio: Optional[datetime] = None,
        vazao: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[VAZMINT, List[VAZMINT], pd.DataFrame]]: ...
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
            return self._as_df(VAZMINT)
        else:
            return self.data.get_registers_of_type(
                VAZMINT, data_inicio=data_inicio, vazao=vazao
            )

    @overload
    def vazmaxt(
        self,
        data_inicio: Optional[datetime] = None,
        vazao: Optional[float] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def vazmaxt(
        self,
        data_inicio: Optional[datetime] = None,
        vazao: Optional[float] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[VAZMAXT, List[VAZMAXT]]]: ...
    @overload
    def vazmaxt(
        self,
        data_inicio: Optional[datetime] = None,
        vazao: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[VAZMAXT, List[VAZMAXT], pd.DataFrame]]: ...
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
            return self._as_df(VAZMAXT)
        else:
            return self.data.get_registers_of_type(
                VAZMAXT, data_inicio=data_inicio, vazao=vazao
            )

    @overload
    def turbmaxt(
        self,
        data_inicio: Optional[datetime] = None,
        turbinamento: Optional[float] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def turbmaxt(
        self,
        data_inicio: Optional[datetime] = None,
        turbinamento: Optional[float] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[TURBMAXT, List[TURBMAXT]]]: ...
    @overload
    def turbmaxt(
        self,
        data_inicio: Optional[datetime] = None,
        turbinamento: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[TURBMAXT, List[TURBMAXT], pd.DataFrame]]: ...
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
            return self._as_df(TURBMAXT)
        else:
            return self.data.get_registers_of_type(
                TURBMAXT, data_inicio=data_inicio, turbinamento=turbinamento
            )

    @overload
    def turbmint(
        self,
        data_inicio: Optional[datetime] = None,
        turbinamento: Optional[float] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def turbmint(
        self,
        data_inicio: Optional[datetime] = None,
        turbinamento: Optional[float] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[TURBMINT, List[TURBMINT]]]: ...
    @overload
    def turbmint(
        self,
        data_inicio: Optional[datetime] = None,
        turbinamento: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[TURBMINT, List[TURBMINT], pd.DataFrame]]: ...
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
            return self._as_df(TURBMINT)
        else:
            return self.data.get_registers_of_type(
                TURBMINT, data_inicio=data_inicio, turbinamento=turbinamento
            )

    @overload
    def cdesvio(
        self,
        codigo_usina_jusante: Optional[int] = None,
        limite_vazao: Optional[float] = None,
        *,
        df: Literal[True],
    ) -> pd.DataFrame: ...
    @overload
    def cdesvio(
        self,
        codigo_usina_jusante: Optional[int] = None,
        limite_vazao: Optional[float] = None,
        df: Literal[False] = False,
    ) -> Optional[Union[CDESVIO, List[CDESVIO]]]: ...
    @overload
    def cdesvio(
        self,
        codigo_usina_jusante: Optional[int] = None,
        limite_vazao: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[CDESVIO, List[CDESVIO], pd.DataFrame]]: ...
    def cdesvio(
        self,
        codigo_usina_jusante: Optional[int] = None,
        limite_vazao: Optional[float] = None,
        df: bool = False,
    ) -> Optional[Union[CDESVIO, List[CDESVIO], pd.DataFrame]]:
        """
        Obtém um registro que define o canal de desvio da usina.

        :param codigo_usina_jusante: a usina a jusante no canal de desvio
        :type codigo_usina_jusante: int | None
        :param limite_vazao: a vazão máxima do canal de desvio em m3/s
        :type limite_vazao: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`CDESVIO` | list[:class:`CDESVIO`] | :class:`pd.DataFrame` | None
        """
        if df:
            return self._as_df(CDESVIO)
        else:
            return self.data.get_registers_of_type(
                CDESVIO,
                codigo_usina_jusante=codigo_usina_jusante,
                limite_vazao=limite_vazao,
            )

    def modificacoes_usina(self, codigo: int) -> Optional[List[Register]]:
        """
        Filtra os registros que são associados a uma usina específica.

        Retorna os registros entre o registro ``USINA`` da usina e o próximo
        ``USINA`` (ou o fim do arquivo). O manual do NEWAVE (seção 3.12)
        admite no máximo um bloco de modificações por usina; se o arquivo
        tiver mais de um bloco para a mesma usina, apenas o primeiro é
        considerado e os demais são ignorados. Para percorrer todos os
        blocos, itere sobre ``self.data`` a partir de cada registro
        ``USINA`` retornado por :meth:`usina`.

        :param codigo: O código da usina
        :type codigo: int
        :return: Os registros que modificam a usina, ou None se o
            arquivo não possuir nenhum registro USINA
        :rtype: List[Register] | None
        """
        usinas = self.data.get_registers_of_type(USINA)
        if usinas is None:
            return None
        if isinstance(usinas, USINA):
            usinas = [usinas]
        reg_usina = next((u for u in usinas if u.codigo == codigo), None)
        modificacoes_usina: List[Register] = []
        if reg_usina is None:
            return modificacoes_usina
        r = reg_usina.next
        while r is not None and not isinstance(r, USINA):
            modificacoes_usina.append(r)
            r = r.next
        return modificacoes_usina
