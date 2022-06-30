from inewave.nwlistop.modelos.coper import CoperAnos

from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import TypeVar, Optional


class Coper(BlockFile):
    """
    Armazena os dados das saídas referentes ao custo total de operação
    de cada estágio em cada série.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `coper.out`.
    """

    T = TypeVar("T")

    BLOCKS = [
        CoperAnos,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__coper = None

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="coper.out") -> "Coper":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="coper.out"):
        self.write(diretorio, nome_arquivo)

    def __monta_tabela(self) -> pd.DataFrame:
        df = None
        for b in self.data.of_type(CoperAnos):
            dados = b.data
            if dados is None:
                continue
            elif df is None:
                df = b.data
            else:
                df = pd.concat([df, b.data], ignore_index=True)
        return df

    @property
    def custos(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os custos por série e
        por mês/ano de estudo.

        :return: A tabela de custos de operação.
        :rtype: Optional[pd.DataFrame]
        """
        if self.__coper is None:
            self.__coper = self.__monta_tabela()
        return self.__coper
