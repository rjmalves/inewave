from inewave.nwlistop.modelos.cdef import CdefAnos

from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
    Submercado,
)

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Cdef(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes ao custo de déficit
    de cada estágio em cada série.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cdef00x.out`.
    """

    BLOCKS = [CdefAnos, Submercado]

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="cdef001.out") -> "Cdef":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
