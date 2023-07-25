from inewave.nwlistop.modelos.gttotsin import GTAnos
from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class GttotSIN(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à geração térmica total
    por patamar, para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `gttotsin.out`.
    """

    BLOCKS = [
        GTAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="gttotsin.out"
    ) -> "GttotSIN":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
