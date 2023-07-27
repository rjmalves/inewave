from inewave.nwlistop.modelos.geolsin import GEAnos

from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Geolsin(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à geração eólica total
    para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `geolsin.out`.
    """

    BLOCKS = [
        GEAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="geolsin.out"
    ) -> "Geolsin":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
