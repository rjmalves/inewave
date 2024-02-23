import pandas as pd  # type: ignore

from cfinterface.files.sectionfile import SectionFile

from inewave.nwlistop.modelos.mediasusit import TabelaMediasusit


class Mediasusit(SectionFile):
    """
    Armazena os dados das saídas referentes às médias de diversas variáveis
    de cada UTE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `MEDIAS-USIT.CSV`.

    """

    SECTIONS = [TabelaMediasusit]

    @property
    def valores(self) -> pd.DataFrame:
        """
        Tabela com os valores de médias para as variáveis das UHE.

        - estagio (`int`)
        - codigo_usina (`int`)
        - <variavel_1> (`float`)
        - ...
        - <variavel_n> (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(TabelaMediasusit)
        if isinstance(b, TabelaMediasusit):
            return b.data
        return None
