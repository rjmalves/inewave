import pandas as pd  # type: ignore[import-untyped]  # no pandas-stubs package

from cfinterface.files.sectionfile import SectionFile

from inewave.nwlistop.modelos.mediassin import TabelaMediassin


class Mediassin(SectionFile):
    """
    Armazena os dados das saídas referentes às médias de diversas variáveis
    para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `MEDIAS-SIN.CSV`.

    """

    SECTIONS = [TabelaMediassin]

    @property
    def valores(self) -> pd.DataFrame:
        """
        Tabela com os valores de médias para as variáveis do SIN.

        - estagio (`int`)
        - <variavel_1> (`float`)
        - ...
        - <variavel_n> (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(TabelaMediassin)
        if isinstance(b, TabelaMediassin):
            return b.data
        return None
