from typing import List

from inewave.nwlistop.modelos.blocos.tabela_medias import TabelaMedias


class TabelaMediasrep(TabelaMedias):
    """
    Bloco com o conteúdo da tabela existente no arquivo `MEDIAS-REP.CSV`.
    """

    __slots__: List[str] = []

    COLUNA_ENTIDADE = "REP_ext"
    NOME_ENTIDADE = "codigo_restricao"
