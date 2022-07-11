from typing import Optional
from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField


class RegistroEolicaSubmercado(Register):
    """
    Registro que contém uma relação entre usina eólica e submercado.
    """

    IDENTIFIER = "EOLICA-SUBMERCADO"
    IDENTIFIER_DIGITS = 17
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
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
    def codigo_submercado(self) -> Optional[int]:
        return self.data[1]

    @codigo_submercado.setter
    def codigo_submercado(self, c: int):
        self.data[1] = c
