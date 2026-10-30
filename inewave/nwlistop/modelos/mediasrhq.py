from typing import List

from inewave.nwlistop.modelos.blocos.tabela_medias import TabelaMedias


class TabelaMediasrhq(TabelaMedias):
    """
    Bloco com o conteúdo da tabela existente no arquivo `MEDIAS-RHQ.CSV`.
    """

    __slots__: List[str] = []

    COLUNA_ENTIDADE = "RHQ_ext"
    NOME_ENTIDADE = "codigo_restricao"
