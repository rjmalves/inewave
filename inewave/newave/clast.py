from inewave.newave.modelos.clast import (
    BlocoUTEClasT,
    BlocoModificacaoUTEClasT,
)

from cfinterface.files.sectionfile import SectionFile
from typing import Type, TypeVar, Optional
import pandas as pd  # type: ignore


class ClasT(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes às classes de
    usinas térmicas.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoUTEClasT, BlocoModificacaoUTEClasT]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="clast.dat") -> "ClasT":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="clast.dat"):
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
    def usinas(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as usinas e seus custos.

        - Número (`int`)
        - Nome (`str`)
        - Tipo Combustível (`str`)
        - Custo [1-5] (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoUTEClasT, 0)
        if b is not None:
            return b.data
        return None

    @usinas.setter
    def usinas(self, valor: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoUTEClasT, 0)
        if b is not None:
            b.data = valor
        else:
            raise ValueError("Campo não lido")

    @property
    def modificacoes(self) -> Optional[pd.DataFrame]:
        """
        Tabela com as modificações de custos das usinas
        organizadas por usina.

        - Número (`int`)
        - Custo (`float`)
        - Mês Início (`int`)
        - Ano Início (`int`)
        - Mês Fim (`int`)
        - Ano Fim (`int`)
        - Nome (`str`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoModificacaoUTEClasT, 0)
        if b is not None:
            return b.data
        return None

    @modificacoes.setter
    def modificacoes(self, valor: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoModificacaoUTEClasT, 0)
        if b is not None:
            b.data = valor
        else:
            raise ValueError("Campo não lido")
