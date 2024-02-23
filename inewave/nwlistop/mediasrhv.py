import pandas as pd  # type: ignore

from cfinterface.files.sectionfile import SectionFile

from inewave.nwlistop.modelos.mediasrhv import TabelaMediasrhv


class Mediasrhv(SectionFile):
    """
    Armazena os dados das saídas referentes às médias
    das restrições hidráulicas de volume.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `MEDIAS-RHV.CSV`.

    """

    SECTIONS = [TabelaMediasrhv]

    @property
    def valores(self) -> pd.DataFrame:
        """
        Tabela com os valores de médias para as variáveis das
        restrições hidráulicas de volume.

        - estagio (`int`)
        - codigo_restricao (`int`)
        - <variavel_1> (`float`)
        - ...
        - <variavel_n> (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(TabelaMediasrhv)
        if isinstance(b, TabelaMediasrhv):
            return b.data
        return None
