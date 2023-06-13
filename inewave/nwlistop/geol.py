from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.geol import GEAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Geol(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à geração eólica total
    por patamar, por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `geol00x.out`, onde x varia conforme o
    PEE em questão.

    """

    BLOCKS = [
        Usina,
        GEAnos,
    ]

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="geol001.out") -> "Geol":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
