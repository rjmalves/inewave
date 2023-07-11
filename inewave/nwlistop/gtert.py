from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivoclassetermicasubmercadopatamar import (
    ArquivoClasseTermicaSubmercadoPatamar,
)
from inewave.nwlistop.modelos.gtert import GTAnos

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Gtert(ArquivoClasseTermicaSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes à geração térmica por classe
    térmica, por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `gtert00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        GTAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="gtert001.out"
    ) -> "Gtert":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))
