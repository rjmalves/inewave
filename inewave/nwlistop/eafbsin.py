from inewave.nwlistop.modelos.eafbsin import EafsAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class EafbSIN(ArquivoSIN):
    """
    Armazena os dados das saídas referentes à energia natural
    afluente para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `eafbsin.out`.
    """

    BLOCKS = [
        EafsAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="eafbsin.out"
    ) -> "EafbSIN":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
