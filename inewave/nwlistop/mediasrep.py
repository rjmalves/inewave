import pandas as pd  # type: ignore

from cfinterface.files.sectionfile import SectionFile

from inewave.nwlistop.modelos.mediasrep import TabelaMediasrep


class Mediasrep(SectionFile):
    """
    Armazena os dados das saídas referentes às médias
    das restrições elétricas especiais.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `MEDIAS-REP.CSV`.

    """

    SECTIONS = [TabelaMediasrep]

    @property
    def valores(self) -> pd.DataFrame:
        """
        Tabela com os valores de médias para as variáveis das
        restrições elétricas especiais.

        - estagio (`int`)
        - codigo_restricao (`int`)
        - <variavel_1> (`float`)
        - ...
        - <variavel_n> (`float`)

        :return: A tabela como um DataFrame
        :rtype: pd.DataFrame | None
        """
        b = self.data.get_sections_of_type(TabelaMediasrep)
        if isinstance(b, TabelaMediasrep):
            return b.data
        return None
