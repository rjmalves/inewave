from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.corteolm import CorteolmAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Corteolm(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes ao corte de geração eólica.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `corteolm00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Submercado,
        CorteolmAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="corteolm001.out"
    ) -> "Corteolm":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
