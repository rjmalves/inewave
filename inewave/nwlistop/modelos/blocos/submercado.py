from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField

from typing import IO


class Submercado(Block):
    """
    Bloco com a informaçao do submercado associado aos valores.
    """

    BEGIN_PATTERN = r"SUBMERCADO:"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(12, 70)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Submercado):
            return False
        bloco: Submercado = o
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
