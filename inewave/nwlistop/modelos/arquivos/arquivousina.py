from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.blocos.valoresserie import (
    ValoresSerie,
)

from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import TypeVar, Optional


class ArquivoUsina(BlockFile):
    """
    Armazena os dados das saídas por usina.
    """

    T = TypeVar("T")

    BLOCKS = [Usina, ValoresSerie]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__valores = None

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="arq.out"
    ) -> "ArquivoUsina":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="arq.out"):
        self.write(diretorio, nome_arquivo)

    def __monta_tabela(self) -> pd.DataFrame:
        df = None
        for b in self.data.of_type(ValoresSerie):
            dados = b.data
            if dados is None:
                continue
            elif df is None:
                df = b.data
            else:
                df = pd.concat([df, b.data], ignore_index=True)
        return df

    @property
    def valores(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os valores, por série e
        por mês/ano de estudo.

        - data (`datetime`)
        - serie (`str`)
        - valor (`float`)

        :return: A tabela dos valores.
        :rtype: pd.DataFrame | None
        """
        if self.__valores is None:
            self.__valores = self.__monta_tabela()
        return self.__valores

    @property
    def usina(self) -> Optional[str]:
        """
        A usina associada ao arquivo lido.

        :return: O nome da usina
        :rtype: str
        """
        b = self.data.get_blocks_of_type(Usina)
        if isinstance(b, Usina):
            return b.data
        return None
