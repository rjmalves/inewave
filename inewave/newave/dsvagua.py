from inewave.newave.modelos.dsvagua import BlocoDsvUHE

from cfinterface.files.sectionfile import SectionFile
from typing import Type, TypeVar, Optional
import pandas as pd  # type: ignore


class DSVAgua(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos
    desvios de água por usina.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que podem ser modificadas através do arquivo `dsvagua.dat`.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoDsvUHE]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="dsvagua.dat"
    ) -> "DSVAgua":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="dsvagua.dat"):
        self.write(diretorio, nome_arquivo)

    def __bloco_por_tipo(self, bloco: Type[T], indice: int) -> Optional[T]:
        """
        Obtém um gerador de blocos de um tipo, se houver algum no arquivo.

        :param bloco: Um tipo de bloco para ser lido
        :type bloco: T
        :param indice: O índice do bloco a ser acessado, dentre os do tipo
        :type indice: int
        :return: O gerador de blocos, se houver
        :rtype: Optional[Generator[T], None, None]
        """
        try:
            return next(
                b
                for i, b in enumerate(self.data.of_type(bloco))
                if i == indice
            )
        except StopIteration:
            return None

    @property
    def desvios(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os desvios de água por usina e por estágio.

        - Ano (`int`)
        - Usina (`int`)
        - Janeiro (`float`)
        - Fevereiro (`float`)
        - ...
        - Dezembro (`float`)
        - Flag (`int`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoDsvUHE, 0)
        if b is not None:
            return b.data
        return None

    @desvios.setter
    def desvios(self, valor: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoDsvUHE, 0)
        if b is not None:
            b.data = valor
        else:
            raise ValueError("Campo não lido")
