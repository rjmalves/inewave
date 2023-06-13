from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.gttot import GTAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Gttot(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes à geração térmica total
    por patamar, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `gttot00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        Submercado,
        GTAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="gttot001.out"
    ) -> "Gttot":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
