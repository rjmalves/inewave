from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.cmarg import CmargsAnos
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Cmarg(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes aos custos marginais de operação
    por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cmarg00x.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        CmargsAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="cmarg001.out"
    ) -> "Cmarg":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
