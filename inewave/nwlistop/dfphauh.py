from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.dfphauh import DfphauhAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Dfphauh(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à variável de folga da
    FPHA da usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dfphauh00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        DfphauhAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="dfphauh001.out"
    ) -> "Dfphauh":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
