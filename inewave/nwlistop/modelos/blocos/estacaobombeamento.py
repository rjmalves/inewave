from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField

from typing import IO


class EstacaoBombeamento(Block):
    """
    Bloco com a informaçao da estação de bombeamento
    associada aos valores.
    """

    __slots__ = ["__linha"]

    BEGIN_PATTERN = r"EST.BOMB.:"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(12, 69)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, EstacaoBombeamento):
            return False
        bloco: EstacaoBombeamento = o
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
    def read(self, file: IO, *args, **kwargs):
        self.data = self.__linha.read(file.readline())[0]
