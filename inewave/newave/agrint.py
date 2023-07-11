from inewave.newave.modelos.agrint import (
    BlocoGruposAgrint,
    BlocoLimitesPorGrupoAgrint,
)

from cfinterface.files.sectionfile import SectionFile
from typing import Type, TypeVar, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Agrint(SectionFile):
    """
    Armazena os dados de entrada do NEWAVE referentes aos agrupamentos
    de intercâmbio.

    """

    T = TypeVar("T")

    SECTIONS = [
        BlocoGruposAgrint,
        BlocoLimitesPorGrupoAgrint,
    ]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="agrint.dat") -> "Agrint":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="agrint.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

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
    def agrupamentos(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os intercâmbios em cada agrupamento.

        - agrupamento (`int`)
        - submercado_de (`int`)
        - submercado_para (`int`)
        - coeficiente (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoGruposAgrint, 0)
        if b is not None:
            return b.data
        return None

    @agrupamentos.setter
    def agrupamentos(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoGruposAgrint, 0)
        if b is not None:
            b.data = df

    @property
    def limites_agrupamentos(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os limites dos agrupamentos de intercâmbio
        durante o período de estudo.

        - agrupamento (`int`)
        - mes_inicio (`int`)
        - ano_inicio (`int`)
        - mes_fim (`int`)
        - ano_fim (`int`)
        - limite_p1 (`float`)
        - limite_p2 (`float`)
        - limite_p3 (`float`)

        :return: A tabela como um DataFrame.
        :rtype: pd.DataFrame | None
        """
        b = self.__bloco_por_tipo(BlocoLimitesPorGrupoAgrint, 0)
        if b is not None:
            return b.data
        return None

    @limites_agrupamentos.setter
    def limites_agrupamentos(self, df: pd.DataFrame):
        b = self.__bloco_por_tipo(BlocoLimitesPorGrupoAgrint, 0)
        if b is not None:
            b.data = df
