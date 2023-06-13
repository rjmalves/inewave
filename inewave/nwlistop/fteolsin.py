from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.exces import ExcesAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class FteolSIN(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à folga da variável de
    geração eólica para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `fteolsin.out`

    """

    BLOCKS = [
        ExcesAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="fteolsin.out"
    ) -> "FteolSIN":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
