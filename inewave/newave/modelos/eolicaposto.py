from typing import Optional
from cfinterface.components.register import Register
from cfinterface.components.line import Line
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField


class RegistroPostoVentoCadastro(Register):
    """
    Registro que contém um cadastro de um posto de vento.
    """

    IDENTIFIER = "POSTO-VENTO-CAD"
    IDENTIFIER_DIGITS = 15
    LINE = Line(
        [
            IntegerField(),
            LiteralField(),
        ],
        delimiter=";",
    )

    @property
    def codigo_posto(self) -> Optional[int]:
        return self.data[0]

    @codigo_posto.setter
    def codigo_posto(self, c: int):
        self.data[0] = c

    @property
    def nome_posto(self) -> Optional[str]:
        return self.data[1]

    @nome_posto.setter
    def nome_posto(self, n: str):
        self.data[1] = n


class RegistroPEEPostoVento(Register):
    """
    Registro que contém um mapeamento de PEE para posto de vento
    """

    IDENTIFIER = "PEE-POSTO"
    IDENTIFIER_DIGITS = 9
    LINE = Line(
        [
            IntegerField(),
            IntegerField(),
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
    def codigo_posto(self) -> Optional[int]:
        return self.data[1]

    @codigo_posto.setter
    def codigo_posto(self, c: int):
        self.data[1] = c
