from inewave.nwlistcf.modelos.nwlistcf import CortesPeriodoNwlistcf

from cfinterface.files.blockfile import BlockFile
from typing import TypeVar, Optional
import pandas as pd  # type: ignore


class Nwlistcf(BlockFile):
    """
    Armazena os dados dos cortes construídos pelo NEWAVE existentes
    no arquivo `nwlistcf.rel` do NWLISTCF.

    Esta classe armazena os cortes da FCF de cada uma das variáveis,
    para cada registro e REE dentro do registro.

    """

    T = TypeVar("T")

    BLOCKS = [CortesPeriodoNwlistcf]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__cortes_periodos = None

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="nwlistcf.rel"
    ) -> "Nwlistcf":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="nwlistcf.rel"):
        self.write(diretorio, nome_arquivo)

    def __monta_tabela_cortes(self) -> pd.DataFrame:
        df = None
        for b in self.data.of_type(CortesPeriodoNwlistcf):
            dados = b.data
            if dados is None:
                continue
            elif df is None:
                df = b.data
            else:
                df = pd.concat([df, b.data], ignore_index=True)
        return df

    @property
    def cortes(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os cortes da FCF.

        - PERIODO (`int`)
        - IREG (`int`)
        - REE (`int`)
        - RHS (`int`)
        - PIV (`int`)
        - PIH 1 (`float`)
        - ...
        - PIH 6 (`float`)
        - PIGTAD(P1L1) (`float`)
        - ...
        - PIGTAD(P3L2) (`float`)
        - PIMX_SAR (`float`)
        - PIMX_CURVA (`float`)

        :return: A tabela de cortes como um DataFrame
        :rtype: pd.DataFrame | None
        """
        if self.__cortes_periodos is None:
            self.__cortes_periodos = self.__monta_tabela_cortes()
        return self.__cortes_periodos
