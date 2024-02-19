from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.gh_fphexat import GhfphexatAnos


class GhFphexat(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à geração hidráulica segundo a
    FPH exata nos pontos de operação da usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `gh_fphexat00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        GhfphexatAnos,
    ]
