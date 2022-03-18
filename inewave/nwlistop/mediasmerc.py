import pandas as pd  # type: ignore

from inewave.nwlistop.modelos.mediasmerc import LeituraMediasMerc


class MediasMerc:
    """
    Armazena os dados das saídas referentes às médias de diversas variáveis
    agrupadas por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `MEDIAS-MERC.CSV`.

    """

    def __init__(self, dados: pd.DataFrame):
        self.__dados = dados

    def __eq__(self, o: object) -> bool:
        """
        A igualdade entre MediasMerc avalia todos os valores da tabela.
        """
        if not isinstance(o, MediasMerc):
            return False
        m: MediasMerc = o
        return self.medias.equals(m.medias)

    @property
    def medias(self) -> pd.DataFrame:
        return self.__dados

    @medias.setter
    def medias(self, d: pd.DataFrame) -> pd.DataFrame:
        self.__dados = d

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="MEDIAS-MERC.CSV"):
        return cls(LeituraMediasMerc(diretorio).le_arquivo(nome_arquivo))
