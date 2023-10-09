from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.ghmax_fpha import GhmaxfphaAnos


class GhmaxFpha(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à geração hidráulica máxima
    no ponto de acesso à FPHA da usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ghmax_fphaXXX.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        GhmaxfphaAnos,
    ]
