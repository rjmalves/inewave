from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.defsin import DefAnos


class Def(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes aos valores de déficit de energia

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `def00XpZ.out`, onde X varia conforme o
    submercado em questão e Z varia conforme o patamar de déficit.

    """

    BLOCKS = [
        Submercado,
        DefAnos,
    ]
