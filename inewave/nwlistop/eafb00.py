from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.eafb00 import EafsAnos
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE


class Eafb00(ArquivoREE):
    """
    Armazena os dados das saídas referentes às energias
    afluentes brutas, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `eafb00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        EafsAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="eafb001.out"
    ) -> "Eafb00":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="eafb001.out"):
        self.write(diretorio, nome_arquivo)
