from typing import List

from inewave.nwlistop.modelos.blocos.tabela_medias import TabelaMedias


class TabelaMediasrhv(TabelaMedias):
    """
    Bloco com o conteúdo da tabela existente no arquivo `MEDIAS-RHV.CSV`.
    """

    __slots__: List[str] = []

    COLUNA_ENTIDADE = "RHV_ext"
    NOME_ENTIDADE = "codigo_restricao"
