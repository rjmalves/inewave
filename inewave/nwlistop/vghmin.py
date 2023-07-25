from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoreepatamar import (
    ArquivoREEPatamar,
)
from inewave.nwlistop.modelos.vghmin import VghminAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Vghmin(ArquivoREEPatamar):
    """
    Armazena os dados das saídas referentes à violação da meta de geração
    hidraulica mínima por patamar, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vghmin00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        VghminAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="vghmin001.out"
    ) -> "Vghmin":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
