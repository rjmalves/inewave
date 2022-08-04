from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE
from inewave.nwlistop.modelos.eaf import EafsAnos


class Eaf(ArquivoREE):
    """
    Armazena os dados das saídas referentes às energias
    afluentes, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `eaf00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        EafsAnos,
    ]

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="eaf001.out") -> "Eaf":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="eaf001.out"):
        self.write(diretorio, nome_arquivo)
