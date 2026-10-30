from typing import List

from inewave.nwlistop.modelos.blocos.tabela_medias import TabelaMedias


class TabelaMediasusih(TabelaMedias):
    """
    Bloco com o conteúdo da tabela existente no arquivo `MEDIAS-USIH.CSV`.
    """

    __slots__: List[str] = []

    COLUNA_ENTIDADE = "USIH_ext"
    NOME_ENTIDADE = "codigo_usina"
