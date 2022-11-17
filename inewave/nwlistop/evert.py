from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE
from inewave.nwlistop.modelos.evert import EvertAnos


class Evert(ArquivoREE):
    """
    Armazena os dados das saídas referentes ao vertimento de reservatórios
    , por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `evert00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        EvertAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="evert001.out"
    ) -> "Evert":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="evert001.out"):
        self.write(diretorio, nome_arquivo)
