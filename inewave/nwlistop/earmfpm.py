from inewave.nwlistop.modelos.earmfpm import EarmsAnos
from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)


class Earmfpm(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes às energias
    armazenadas finais, por submercado e em % da energia armazenável máxima.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `earmfpm00x.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        EarmsAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="earmfpm001.out"
    ) -> "Earmfpm":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="earmfpm001.out"):
        self.write(diretorio, nome_arquivo)
