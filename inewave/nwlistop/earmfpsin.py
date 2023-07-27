from inewave.nwlistop.modelos.earmfpsin import EarmsAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Earmfpsin(ArquivoSIN):
    """
    Armazena os dados das saídas referentes às energias
    armazenadas finais para o SIN e em % da energia armazenável máxima.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `earmfpsin.out`, onde x varia conforme o
    submercado em questão.
    """

    BLOCKS = [
        EarmsAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="earmfpsin.out"
    ) -> "Earmfpsin":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
