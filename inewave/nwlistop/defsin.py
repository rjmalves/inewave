from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.defsin import DefAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class DefSIN(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes ao déficit
    por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `defsinp001.out`.
    """

    BLOCKS = [
        DefAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="defsinp001.out"
    ) -> "DefSIN":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
