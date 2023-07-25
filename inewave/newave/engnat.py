from cfinterface.files.sectionfile import SectionFile
from inewave.newave.modelos.engnat import SecaoDadosEngnat
import pandas as pd  # type: ignore

from typing import TypeVar, Optional

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Engnat(SectionFile):
    """
    Armazena os dados de saída do NEWAVE referentes às séries históricas
    de energia por configuração, calculadas a partir das séries históricas
    de vazão.
    """

    T = TypeVar("T")

    SECTIONS = [SecaoDadosEngnat]
    STORAGE = "BINARY"

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(
        cls,
        diretorio: str,
        nome_arquivo="engnat.dat",
        numero_rees: int = 12,
        numero_configuracoes: int = 60,
        ano_inicio_historico: int = 1931,
    ) -> "Engnat":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(
            join(diretorio, nome_arquivo),
            numero_rees=numero_rees,
            numero_configuracoes=numero_configuracoes,
            ano_inicio_historico=ano_inicio_historico,
        )

    @property
    def series(self) -> Optional[pd.DataFrame]:
        """
        Obtém a tabela com os dados das séries de energia
        afluente por REE e por estágio.

        - configuracao (`int`): configuração da série histórica
        - data (`datetime`): data para o valor histórico
        - ree (`int`): REE para o qual foi gerado
        - valor (`float`): energia em MWmes

        :return: A tabela com os dados das séries
        :rtype: pd.DataFrame | None
        """
        sections = [r for r in self.data.of_type(SecaoDadosEngnat)]
        if len(sections) > 0:
            return sections[0].data
        else:
            return None

    @series.setter
    def series(self, df: pd.DataFrame):
        sections = [r for r in self.data.of_type(SecaoDadosEngnat)]
        if len(sections) > 0:
            sections[0].data = df
