import pandas as pd  # type: ignore

from cfinterface.files.sectionfile import SectionFile

from inewave.nwlistop.modelos.mediasree import TabelaMediasree


class Mediasree(SectionFile):
    """
    Armazena os dados das saídas referentes às médias de diversas variáveis
    agrupadas por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `MEDIAS-REE.CSV`.

    """

    SECTIONS = [TabelaMediasree]

    @property
    def valores(self) -> pd.DataFrame:
        """
        Tabela com os valores de médias para as variáveis dos REE.

        - estagio (`int`)
        - codigo_ree (`int`)
        - <variavel_1> (`float`)
        - ...
        - <variavel_n> (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(TabelaMediasree)
        if isinstance(b, TabelaMediasree):
            return b.data
        return None
