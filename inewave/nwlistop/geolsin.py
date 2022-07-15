from inewave.nwlistop.modelos.geolsin import GEAnos

from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import TypeVar, Optional


class GeolSIN(BlockFile):
    """
    Armazena os dados das saídas referentes à geração eólica total
    para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `geolsin.out`.
    """

    T = TypeVar("T")

    BLOCKS = [
        GEAnos,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__gh = None

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="geolsin.out"
    ) -> "GeolSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="geolsin.out"):
        self.write(diretorio, nome_arquivo)

    def __monta_tabela(self) -> pd.DataFrame:
        df = None
        for b in self.data.of_type(GEAnos):
            dados = b.data
            if dados is None:
                continue
            elif df is None:
                df = b.data
            else:
                df = pd.concat([df, b.data], ignore_index=True)
        return df

    @property
    def geracao(self) -> Optional[pd.DataFrame]:
        """
        Tabela com a geracao eólica por série e
        por mês/ano de estudo.

        - Ano (`int`)
        - Série (`int`)
        - Patamar (`str`)
        - Janeiro (`float`)
        - ...
        - Dezembro (`float`)

        :return: A tabela da geração eólica.
        :rtype: pd.DataFrame | None
        """
        if self.__gh is None:
            self.__gh = self.__monta_tabela()
        return self.__gh
