from inewave.nwlistop.modelos.blocos.parsubmercados import ParSubmercados
from inewave.nwlistop.modelos.arquivos.arquivoparsubmercadopatamar import (
    ArquivoParSubmercadoPatamar,
)
from inewave.nwlistop.modelos.intercambio import IntercambioAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Intercambio(ArquivoParSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes ao intercâmbio
    por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `int00x00y.out`, onde x e y variam
    conforme os submercados em questão.

    """

    BLOCKS = [
        ParSubmercados,
        IntercambioAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="int001002.out"
    ) -> "Intercambio":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
