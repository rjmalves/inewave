from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.exces import ExcesAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Fteolm(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes à folga da variável de
    geração eólica por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `fteolm00x.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        ExcesAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="fteolm001.out"
    ) -> "Fteolm":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
