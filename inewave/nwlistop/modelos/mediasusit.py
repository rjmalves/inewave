from typing import List

from inewave.nwlistop.modelos.blocos.tabela_medias import TabelaMedias


class TabelaMediasusit(TabelaMedias):
    """
    Bloco com o conteúdo da tabela existente no arquivo `MEDIAS-USIT.CSV`.
    """

    __slots__: List[str] = []

    COLUNA_ENTIDADE = "USIT_ext"
    NOME_ENTIDADE = "codigo_usina"
