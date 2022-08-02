from inewave.nwlistop.modelos.earmfpsin import EarmsAnos

from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import TypeVar, Optional


class EarmfpSIN(BlockFile):
    """
    Armazena os dados das saídas referentes às energias
    armazenadas finais para o SIN e em % da energia armazenável máxima.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `earmfpsin.out`, onde x varia conforme o
    submercado em questão.
    """

    T = TypeVar("T")

    BLOCKS = [
        EarmsAnos,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__earms = None

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="earmfpsin.out"
    ) -> "EarmfpSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="earmfpsin.out"):
        self.write(diretorio, nome_arquivo)

    def __monta_tabela(self) -> pd.DataFrame:
        df = None
        for b in self.data.of_type(EarmsAnos):
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
        Tabela com as energias armazenadas percentuais por série e
        por mês/ano de estudo.

        - Ano (`int`)
        - Série (`int`)
        - Janeiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: A tabela das energias armazenadas.
        :rtype: pd.DataFrame
        """
        if self.__earms is None:
            self.__earms = self.__monta_tabela()
        return self.__earms
