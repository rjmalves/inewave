from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE

from inewave.nwlistop.modelos.verturb import VertAnos


class Verturb(ArquivoREE):
    """
    Armazena os dados das saídas referentes às energias
    vertidas, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vertub00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        VertAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="verturb001.out"
    ) -> "Verturb":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="verturb001.out"):
        self.write(diretorio, nome_arquivo)
