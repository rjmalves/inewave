from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField

from typing import IO, Any, Optional


class REE(Block):
    """
    Bloco com a informaçao do REE associado aos valores.
    """

    __slots__ = ["__linha"]

    BEGIN_PATTERN = r"REE:"
    END_PATTERN = ""

    def __init__(
        self,
        previous: Optional[Any] = None,
        next: Optional[Any] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(12, 63)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, REE):
            return False
        bloco: REE = o
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
    def read(self, file: IO[Any], *args: Any, **kwargs: Any) -> None:  # type: ignore[override]  # signature extends base class
        self.data = self.__linha.read(file.readline())[0]
