from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)
from inewave.nwlistop.modelos.gttot00 import GTAnos


class Gttot00(ArquivoSubmercado):
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
    ) -> "Gttot00":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="gttot001.out"):
        self.write(diretorio, nome_arquivo)
