from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField

from typing import IO


class Restricao(Block):
    """
    Bloco com a informaçao da restrição associada aos valores.
    """

    __slots__ = ["__linha"]

    BEGIN_PATTERN = r"RESTRICAO:"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([IntegerField(4, 69)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Restricao):
            return False
        bloco: Restricao = o
        if not all(
            [
                isinstance(self.data, int),
                isinstance(o.data, int),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    # Override
    def read(self, file: IO, *args, **kwargs):
        self.data = self.__linha.read(file.readline())[0]
