import pandas as pd  # type: ignore

from cfinterface.files.sectionfile import SectionFile

from inewave.nwlistop.modelos.mediasusie import TabelaMediasusie


class Mediasusie(SectionFile):
    """
    Armazena os dados das saídas referentes às médias de diversas variáveis
    de cada estação elevatória.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `MEDIAS-USIE.CSV`.

    """

    SECTIONS = [TabelaMediasusie]

    @property
    def valores(self) -> pd.DataFrame:
        """
        Tabela com os valores de médias para as variáveis das estações
        elevatórias.

        - estagio (`int`)
        - codigo_usina (`int`)
        - <variavel_1> (`float`)
        - ...
        - <variavel_n> (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(TabelaMediasusie)
        if isinstance(b, TabelaMediasusie):
            return b.data
        return None
