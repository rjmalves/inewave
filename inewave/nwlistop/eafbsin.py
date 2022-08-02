from inewave.nwlistop.modelos.eafbsin import EafAnos

from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import TypeVar, Optional


class EafbSIN(BlockFile):
    """
    Armazena os dados das saídas referentes à energia natural
    afluente para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `eafbsin.out`.
    """

    T = TypeVar("T")

    BLOCKS = [
        EafAnos,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__earm = None

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="eafbsin.out"
    ) -> "EafbSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="eafbsin.out"):
        self.write(diretorio, nome_arquivo)

    def __monta_tabela(self) -> pd.DataFrame:
        df = None
        for b in self.data.of_type(EafAnos):
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
        Tabela com as energias por série e
        por mês/ano de estudo.

        - Ano (`int`)
        - Série (`int`)
        - Janeiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: A tabela de energia afluente.
        :rtype: pd.DataFrame
        """
        if self.__earm is None:
            self.__earm = self.__monta_tabela()
        return self.__earm
