from typing import IO, Any, List, Optional, Union

from cfinterface.components.line import Line
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.register import Register
from cfinterface.storage import StorageType


class RegistroIndice(Register):
    """
    Registro do arquivo de índices das LIBS, que associa o identificador
    de um card das LIBS ao arquivo que contém os seus registros, no
    formato ``IDENTIFICADOR;DESCRICAO;ARQUIVO``.

    O registro não possui um identificador fixo: o primeiro campo da
    linha é o próprio identificador do card indexado.
    """

    __slots__: List[str] = []

    IDENTIFIER = ""
    IDENTIFIER_DIGITS = 0
    LINE = Line(
        [
            LiteralField(size=200),
            LiteralField(size=200),
            LiteralField(size=200),
        ],
        delimiter=";",
    )

    @classmethod
    def matches(
        cls, line: Union[str, bytes], storage: Union[str, StorageType] = ""
    ) -> bool:
        """
        Casa as linhas que contêm ``;`` e que não são comentários, isto é,
        que não começam com ``&`` após os espaços iniciais.
        """
        if isinstance(line, bytes):
            return b";" in line and not line.lstrip().startswith(b"&")
        return ";" in line and not line.lstrip().startswith("&")

    def read(
        self,
        file: IO[Any],
        storage: Union[str, StorageType] = "",
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        self.data = self.__class__.LINE.read(file.readline())
        return True

    def write(
        self,
        file: IO[Any],
        storage: Union[str, StorageType] = "",
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        file.write(self.__class__.LINE.write(self.data))
        return True

    @property
    def identificador(self) -> Optional[str]:
        """
        O identificador do card das LIBS.

        :return: O identificador
        :rtype: str | None
        """
        return self.data[0]

    @identificador.setter
    def identificador(self, i: str) -> None:
        self.data[0] = i

    @property
    def descricao(self) -> Optional[str]:
        """
        A descrição do card das LIBS.

        :return: A descrição
        :rtype: str | None
        """
        return self.data[1]

    @descricao.setter
    def descricao(self, d: str) -> None:
        self.data[1] = d

    @property
    def arquivo(self) -> Optional[str]:
        """
        O arquivo que contém os registros do card das LIBS.

        :return: O nome do arquivo
        :rtype: str | None
        """
        return self.data[2]

    @arquivo.setter
    def arquivo(self, a: str) -> None:
        self.data[2] = a
