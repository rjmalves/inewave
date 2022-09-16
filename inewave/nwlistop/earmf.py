from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE

from inewave.nwlistop.modelos.earmf import EarmsAnos


class Earmf(ArquivoREE):
    """
    Armazena os dados das saídas referentes às energias
    armazenadas finais, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `earmf00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        EarmsAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="earmf001.out"
    ) -> "Earmf":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="earmf001.out"):
        self.write(diretorio, nome_arquivo)
