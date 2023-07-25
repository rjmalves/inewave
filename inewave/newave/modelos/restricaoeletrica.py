from typing import Optional
from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from cfinterface.components.datetimefield import DatetimeField
from datetime import datetime


class RegistroRE(Register):
    """
    Registro que contém um cadastro de restrição elétrica (RE).
    """

    IDENTIFIER = "RE"
    IDENTIFIER_DIGITS = 2
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


class RegistroREHorizPer(Register):
    """
    Registro que contém o cadastro do horizonte de validade
    da restrição RE.
    """

    IDENTIFIER = "RE-HORIZ-PER"
    IDENTIFIER_DIGITS = 12
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


class RegistroRELimFormPer(Register):
    """
    Registro que contém os limites de cada restrição
    RE por patamar.
    """

    IDENTIFIER = "RE-LIM-FORM-PER"
    IDENTIFIER_DIGITS = 15
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            IntegerField(),
            FloatField(size=16, decimal_digits=4, format="e"),
            FloatField(size=16, decimal_digits=4, format="e"),
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
    def data_final(self, v: datetime):
        self.data[2] = v

    @property
    def patamar(self) -> Optional[int]:
        return self.data[3]

    @patamar.setter
    def patamar(self, v: int):
        self.data[3] = v

    @property
    def limite_inferior(self) -> Optional[float]:
        return self.data[4]

    @limite_inferior.setter
    def limite_inferior(self, v: float):
        self.data[4] = v

    @property
    def limite_superior(self) -> Optional[float]:
        return self.data[5]

    @limite_superior.setter
    def limite_superior(self, v: float):
        self.data[5] = v
