from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE

from inewave.nwlistop.modelos.verturb import VertAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Verturb(ArquivoREE):
    """
    Armazena os dados das saídas referentes às energias
    vertidas, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vertub00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        VertAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="verturb001.out"
    ) -> "Verturb":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
