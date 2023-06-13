from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoreepatamar import (
    ArquivoREEPatamar,
)
from inewave.nwlistop.modelos.dlppdfmax import DLPPdfmaxAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class DLPPdfmax(ArquivoREEPatamar):
    """
    Armazena os dados das saídas referentes à violação das restrições LPP
    de defluência máxima por patamar, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dlppdfmax00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        DLPPdfmaxAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="dlppdfmax001.out"
    ) -> "DLPPdfmax":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
