from typing import Optional
from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.datetimefield import DatetimeField
from datetime import datetime


class RegistroEolicaConfiguracao(Register):
    """
    Registro que contém um estado de operação de uma usina por
    período.
    """

    IDENTIFIER = "EOLICA-CONFIGURACAO-PERIODO"
    IDENTIFIER_DIGITS = 27
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            LiteralField(),
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
    def data_inicial_estado_operacao(self) -> Optional[datetime]:
        return self.data[1]

    @data_inicial_estado_operacao.setter
    def data_inicial_estado_operacao(self, n: datetime):
        self.data[1] = n

    @property
    def data_final_estado_operacao(self) -> Optional[datetime]:
        return self.data[2]

    @data_final_estado_operacao.setter
    def data_final_estado_operacao(self, n: datetime):
        self.data[2] = n

    @property
    def estado_operacao(self) -> Optional[str]:
        return self.data[3]

    @estado_operacao.setter
    def estado_operacao(self, n: str):
        self.data[3] = n
