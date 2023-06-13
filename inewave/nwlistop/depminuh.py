from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.depminuh import DepminAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Depminuh(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes À violação de defluência
    mínima da usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `depminuh00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        DepminAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="depminuh001.out"
    ) -> "Depminuh":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
