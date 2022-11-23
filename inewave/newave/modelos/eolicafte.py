from typing import Optional
from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.datetimefield import DatetimeField
from cfinterface.components.floatfield import FloatField
from datetime import datetime


class RegistroEolicaFTE(Register):
    """
    Registro que contém as informações da função de produção
    linear vento-potência para as usinas eólicas.
    """

    IDENTIFIER = "EOLICA-FUNCAO-PRODUCAO-VENTO-POTENCIA-LINEAR-PU-PERIODO"
    IDENTIFIER_DIGITS = 55
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(decimal_digits=8),
            FloatField(decimal_digits=8),
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
    def coeficiente_linear(self) -> Optional[float]:
        return self.data[3]

    @coeficiente_linear.setter
    def coeficiente_linear(self, c: float):
        self.data[3] = c

    @property
    def coeficiente_angular(self) -> Optional[float]:
        return self.data[4]

    @coeficiente_angular.setter
    def coeficiente_angular(self, c: float):
        self.data[4] = c


class RegistroPEEFTE(Register):
    """
    Registro que contém as informações da função de produção
    linear vento-potência para um PEE.
    """

    IDENTIFIER = "PEE-FPVP-LIN-PU-PER"
    IDENTIFIER_DIGITS = 19
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(size=20, decimal_digits=17),
            FloatField(size=20, decimal_digits=17),
        ],
        delimiter=";",
    )

    @property
    def codigo_pee(self) -> Optional[int]:
        return self.data[0]

    @codigo_pee.setter
    def codigo_pee(self, c: int):
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
    def coeficiente_linear(self) -> Optional[float]:
        return self.data[3]

    @coeficiente_linear.setter
    def coeficiente_linear(self, c: float):
        self.data[3] = c

    @property
    def coeficiente_angular(self) -> Optional[float]:
        return self.data[4]

    @coeficiente_angular.setter
    def coeficiente_angular(self, c: float):
        self.data[4] = c
