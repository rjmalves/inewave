import pandas as pd  # type: ignore

from cfinterface.files.sectionfile import SectionFile

from inewave.nwlistop.modelos.mediasmerc import TabelaMediasmerc


class Mediasmerc(SectionFile):
    """
    Armazena os dados das saídas referentes às médias de diversas variáveis
    agrupadas por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `MEDIAS-MERC.CSV`.

    """

    SECTIONS = [TabelaMediasmerc]

    @property
    def valores(self) -> pd.DataFrame:
        """
        Tabela com os valores de médias para as variáveis dos submercados.

        - estagio (`int`)
        - codigo_submercado (`int`)
        - <variavel_1> (`float`)
        - ...
        - <variavel_n> (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(TabelaMediasmerc)
        if isinstance(b, TabelaMediasmerc):
            return b.data
        return None
