from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)
from inewave.nwlistop.modelos.evertsin import EvertAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class EvertSIN(ArquivoSIN):
    """
    Armazena os dados das saídas referentes ao vertimento de reservatórios
    , para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `evertsin.out`.

    """

    BLOCKS = [
        EvertAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="evertsin.out"
    ) -> "EvertSIN":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
