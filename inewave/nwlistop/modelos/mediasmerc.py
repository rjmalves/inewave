from typing import List

from inewave.nwlistop.modelos.blocos.tabela_medias import TabelaMedias


class TabelaMediasmerc(TabelaMedias):
    """
    Bloco com o conteúdo da tabela existente no arquivo `MEDIAS-MERC.CSV`.
    """

    __slots__: List[str] = []

    COLUNA_ENTIDADE = "SBM_ext"
    NOME_ENTIDADE = "codigo_submercado"
