from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.dlppdfmax import DLPPdfmaxAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class DLPPtbmaxm(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes à violação das restrições LPP
    de turbinamento máximo por patamar, por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dlpptbmax00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        DLPPdfmaxAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="dlpptbmaxm001.out"
    ) -> "DLPPtbmaxm":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
