from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)
from inewave.nwlistop.modelos.eafm import EafsAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Eafm(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes às energias
    afluentes, por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `eaf00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        EafsAnos,
    ]

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="eafm001.out") -> "Eafm":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
