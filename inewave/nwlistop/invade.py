from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE
from inewave.nwlistop.modelos.invade import InvadeAnos


class Invade(ArquivoREE):
    """
    Armazena os dados das saídas referentes às violações da CAR
    , por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `invade00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        InvadeAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="invade001.out"
    ) -> "Invade":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="invade001.out"):
        self.write(diretorio, nome_arquivo)
