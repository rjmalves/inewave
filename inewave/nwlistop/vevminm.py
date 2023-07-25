from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)
from inewave.nwlistop.modelos.vevminm import VevminAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Vevminm(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes às violações da meta
    de energia da vazão mínima, por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vevminm00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        VevminAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="vevminm001.out"
    ) -> "Vevminm":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
