from typing import List

from inewave.nwlistop.modelos.blocos.tabela_medias import TabelaMedias


class TabelaMediasusie(TabelaMedias):
    """
    Bloco com o conteúdo da tabela existente no arquivo `MEDIAS-USIE.CSV`.
    """

    __slots__: List[str] = []

    COLUNA_ENTIDADE = "USIE_ext"
    NOME_ENTIDADE = "codigo_usina"
