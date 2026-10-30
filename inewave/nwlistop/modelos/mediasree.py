from typing import List

from inewave.nwlistop.modelos.blocos.tabela_medias import TabelaMedias


class TabelaMediasree(TabelaMedias):
    """
    Bloco com o conteúdo da tabela existente no arquivo `MEDIAS-REE.CSV`.
    """

    __slots__: List[str] = []

    COLUNA_ENTIDADE = "REE_ext"
    NOME_ENTIDADE = "codigo_ree"
