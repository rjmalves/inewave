from cfinterface.components.block import Block
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.line import Line

from typing import IO


class VersaoModelo(Block):
    """
    Bloco para ler a versão utilizada do modelo a partir da linha de
    título do arquivo.
    """

    BEGIN_PATTERN = r"CEPEL: NEWAVE"
    END_PATTERN = ""

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, VersaoModelo):
            return False
        else:
            if not all([type(self.data) is str, type(o.data) is str]):
                return False
            return self.data == o.data

    def read(self, file: IO, *args, **kwargs):
        linha = file.readline()
        modelo_linha = Line([LiteralField(size=12, starting_position=29)])
        self.data = modelo_linha.read(linha)[0]
