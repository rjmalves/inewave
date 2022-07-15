from inewave.newave.modelos.vazpast import BlocoVazPast

from cfinterface.files.sectionfile import SectionFile
from typing import Type, TypeVar, Optional
import pandas as pd  # type: ignore


class VazPast(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às
    vazões anteriores ao período de planejamento.

    Esta classe lida com informações de entrada fornecidas ao NEWAVE e
    que são usadas juntos das contidas no arquivo `vazoes.dat`.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoVazPast]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="vazpast.dat"
    ) -> "VazPast":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="vazpast.dat"):
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
    def tendencia(self) -> Optional[pd.DataFrame]:
        """
        Tabela com a tendência hidrológica por REE.

        - Índice (`int`)
        - Usina (`str`)
        - Janeiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoVazPast, 0)
        if b is not None:
            return b.data
        return None

    @tendencia.setter
    def tendencia(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoVazPast, 0)
        if b is not None:
            b.data = df
