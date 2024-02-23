import pandas as pd  # type: ignore

from cfinterface.files.sectionfile import SectionFile

from inewave.nwlistop.modelos.mediasrhq import TabelaMediasrhq


class Mediasrhq(SectionFile):
    """
    Armazena os dados das saídas referentes às médias
    das restrições hidráulicas de vazão.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `MEDIAS-RHQ.CSV`.

    """

    SECTIONS = [TabelaMediasrhq]

    @property
    def valores(self) -> pd.DataFrame:
        """
        Tabela com os valores de médias para as variáveis das
        restrições hidráulicas de vazão.

        - estagio (`int`)
        - codigo_restricao (`int`)
        - <variavel_1> (`float`)
        - ...
        - <variavel_n> (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(TabelaMediasrhq)
        if isinstance(b, TabelaMediasrhq):
            return b.data
        return None
