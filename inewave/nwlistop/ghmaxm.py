from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.ghmaxm import GHAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Ghmaxm(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes à geração hidraulica máxima
    por patamar, por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ghmax00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        GHAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="ghmaxm001.out"
    ) -> "Ghmaxm":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
