from typing import Optional
from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.datetimefield import DatetimeField
from cfinterface.components.floatfield import FloatField
from datetime import datetime


class RegistroEolicaHistoricoVentoHorizonte(Register):
    """
    Registro que contém o horizonte de históricos de vento.
    """

    IDENTIFIER = "EOLICA-HISTORICO-VENTO-HORIZONTE"
    IDENTIFIER_DIGITS = 32
    LINE = Line(
        [
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
        ],
        delimiter=";",
    )

    @property
    def data_inicial(self) -> Optional[datetime]:
        return self.data[0]

    @data_inicial.setter
    def data_inicial(self, c: datetime):
        self.data[0] = c

    @property
    def data_final(self) -> Optional[datetime]:
        return self.data[1]

    @data_final.setter
    def data_final(self, c: datetime):
        self.data[1] = c


class RegistroEolicaHistoricoVento(Register):
    """
    Registro que contém os históricos de vento para o horizonte
    considerado.
    """

    IDENTIFIER = "EOLICA-HISTORICO-VENTO"
    IDENTIFIER_DIGITS = 22
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(decimal_digits=2),
            FloatField(decimal_digits=2),
        ],
        delimiter=";",
    )

    @property
    def codigo_eolica(self) -> Optional[int]:
        return self.data[0]

    @codigo_eolica.setter
    def codigo_eolica(self, c: int):
        self.data[0] = c

    @property
    def data_inicial(self) -> Optional[datetime]:
        return self.data[1]

    @data_inicial.setter
    def data_inicial(self, c: datetime):
        self.data[1] = c

    @property
    def data_final(self) -> Optional[datetime]:
        return self.data[2]

    @data_final.setter
    def data_final(self, c: datetime):
        self.data[2] = c

    @property
    def velocidade(self) -> Optional[float]:
        return self.data[3]

    @velocidade.setter
    def velocidade(self, c: float):
        self.data[3] = c

    @property
    def direcao(self) -> Optional[float]:
        return self.data[4]

    @direcao.setter
    def direcao(self, c: float):
        self.data[4] = c


class RegistroHistoricoVentoHorizonte(Register):
    """
    Registro que contém o horizonte de históricos de vento.
    """

    IDENTIFIER = "VENTO-HIST-HORIZ"
    IDENTIFIER_DIGITS = 16
    LINE = Line(
        [
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
        ],
        delimiter=";",
    )

    @property
    def data_inicial(self) -> Optional[datetime]:
        return self.data[0]

    @data_inicial.setter
    def data_inicial(self, c: datetime):
        self.data[0] = c

    @property
    def data_final(self) -> Optional[datetime]:
        return self.data[1]

    @data_final.setter
    def data_final(self, c: datetime):
        self.data[1] = c


class RegistroHistoricoVento(Register):
    """
    Registro que contém os históricos de vento para o horizonte
    considerado em um PEE.
    """

    IDENTIFIER = "VENTO-HIST"
    IDENTIFIER_DIGITS = 10
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(decimal_digits=2),
            FloatField(decimal_digits=2),
        ],
        delimiter=";",
    )

    @property
    def codigo_posto(self) -> Optional[int]:
        return self.data[0]

    @codigo_posto.setter
    def codigo_posto(self, c: int):
        self.data[0] = c

    @property
    def data_inicial(self) -> Optional[datetime]:
        return self.data[1]

    @data_inicial.setter
    def data_inicial(self, c: datetime):
        self.data[1] = c

    @property
    def data_final(self) -> Optional[datetime]:
        return self.data[2]

    @data_final.setter
    def data_final(self, c: datetime):
        self.data[2] = c

    @property
    def velocidade(self) -> Optional[float]:
        return self.data[3]

    @velocidade.setter
    def velocidade(self, c: float):
        self.data[3] = c

    @property
    def direcao(self) -> Optional[float]:
        return self.data[4]

    @direcao.setter
    def direcao(self, c: float):
        self.data[4] = c
