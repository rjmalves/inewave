from typing import Optional
from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.datetimefield import DatetimeField
from datetime import datetime


class RegistroRHQ(Register):
    """
    Registro que contém um cadastro de restrição de
    vazão (RHQ).
    """

    IDENTIFIER = "RHQ"
    IDENTIFIER_DIGITS = 3
    LINE = Line(
        [
            IntegerField(),
            LiteralField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def formula(self) -> Optional[str]:
        return self.data[1]

    @formula.setter
    def formula(self, n: str):
        self.data[1] = n


class RegistroRHQHorizPer(Register):
    """
    Registro que contém o cadastro do horizonte de validade
    da restrição RHQ.
    """

    IDENTIFIER = "RHQ-HORIZ-PER"
    IDENTIFIER_DIGITS = 13
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
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
    def data_final(self, n: datetime):
        self.data[2] = n


class RegistroRHQLsLPPVoli(Register):
    """
    Registro que contém as retas de cada restrição
    RHQ modelada como restrição linear por partes.
    """

    IDENTIFIER = "RHQ-LS-LPP-VOLI"
    IDENTIFIER_DIGITS = 15
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
            FloatField(size=16, decimal_digits=4),
            FloatField(size=16, decimal_digits=4),
        ],
        delimiter=";",
    )

    @property
    def codigo_restricao(self) -> Optional[int]:
        return self.data[0]

    @codigo_restricao.setter
    def codigo_restricao(self, c: int):
        self.data[0] = c

    @property
    def indice_reta(self) -> Optional[int]:
        return self.data[1]

    @indice_reta.setter
    def indice_reta(self, c: int):
        self.data[1] = c

    @property
    def coeficiente_angular(self) -> Optional[float]:
        return self.data[2]

    @coeficiente_angular.setter
    def coeficiente_angular(self, v: float):
        self.data[2] = v

    @property
    def coeficiente_linear(self) -> Optional[float]:
        return self.data[3]

    @coeficiente_linear.setter
    def coeficiente_linear(self, v: float):
        self.data[3] = v
