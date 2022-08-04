from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE

from inewave.nwlistop.modelos.vagua import VAAnos


class Vagua(ArquivoREE):
    """
    Armazena os dados das saídas referentes aos valores da água
    por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vagua00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        VAAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="vagua001.out"
    ) -> "Vagua":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="vagua001.out"):
        self.write(diretorio, nome_arquivo)
