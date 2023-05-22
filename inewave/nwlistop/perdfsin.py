from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.perdfsin import PerdfAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class PerdfSIN(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao vertimento fio d'água
    , para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `perdfsin.out`.

    """

    BLOCKS = [
        PerdfAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="perdfsin.out"
    ) -> "PerdfSIN":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
