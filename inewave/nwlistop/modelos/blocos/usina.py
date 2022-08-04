from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField

from typing import IO


class Usina(Block):
    """
    Bloco com a informaçao da usina associado aos valores.
    """

    BEGIN_PATTERN = r"USINA:"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(12, 65)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Usina):
            return False
        bloco: Usina = o
        if not all(
            [
                isinstance(self.data, str),
                isinstance(o.data, str),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    # Override
    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())[0]
