from typing import Optional
from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.datetimefield import DatetimeField
from cfinterface.components.floatfield import FloatField
from datetime import datetime


class RegistroEolicaGeracaoPeriodo(Register):
    """
    Registro que contém os valores de geração de uma usina
    eólica.
    """

    IDENTIFIER = "EOLICA-GERACAO-PERIODO"
    IDENTIFIER_DIGITS = 22
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            FloatField(),
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


class RegistroEolicaGeracaoPatamar(Register):
    """
    Registro que contém as profundidades dos patamares de cada
    período para o histórico de geração.
    """

    IDENTIFIER = "EOLICA-GERACAO-PROFUNDIDADE-PERIODO-PATAMAR"
    IDENTIFIER_DIGITS = 43
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            IntegerField(),
            FloatField(decimal_digits=4),
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
    def indice_patamar(self) -> Optional[int]:
        return self.data[3]

    @indice_patamar.setter
    def indice_patamar(self, c: int):
        self.data[3] = c

    @property
    def profundidade(self) -> Optional[float]:
        return self.data[4]

    @profundidade.setter
    def profundidade(self, c: float):
        self.data[4] = c


class RegistroPEEGeracaoPatamar(Register):
    """
    Registro que contém as profundidades dos patamares de cada
    período para o histórico de geração de um PEE.
    """

    IDENTIFIER = "PEE-GER-PROF-PER-PAT"
    IDENTIFIER_DIGITS = 20
    LINE = Line(
        [
            IntegerField(),
            DatetimeField(size=7, format="%Y/%m"),
            DatetimeField(size=7, format="%Y/%m"),
            IntegerField(),
            FloatField(decimal_digits=4),
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
    def indice_patamar(self) -> Optional[int]:
        return self.data[3]

    @indice_patamar.setter
    def indice_patamar(self, c: int):
        self.data[3] = c

    @property
    def profundidade(self) -> Optional[float]:
        return self.data[4]

    @profundidade.setter
    def profundidade(self, c: float):
        self.data[4] = c
