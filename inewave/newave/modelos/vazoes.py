from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from typing import List


class RegistroVazoesPostos(Register):
    """
    Registro com os dados associados às vazões dos postos.
    """

    POSTOS = 320

    LINE = Line(
        [IntegerField(size=4, starting_position=4 * i) for i in range(POSTOS)],
        storage="BINARY",
    )

    @classmethod
    def set_postos(cls, postos: int):
        cls.POSTOS = postos
        cls.LINE = Line(
            [
                IntegerField(size=4, starting_position=4 * i)
                for i in range(postos)
            ],
            storage="BINARY",
        )

    @property
    def vazoes(self) -> List[int]:
        return self.data

    @vazoes.setter
    def vazoes(self, v: List[int]):
        self.data = v
