from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE
from inewave.nwlistop.modelos.perdf import PerdfAnos


class Perdf(ArquivoREE):
    """
    Armazena os dados das saídas referentes ao vertimento fio d'água
    , por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `perdf00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        PerdfAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="perdf001.out"
    ) -> "Perdf":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="perdf001.out"):
        self.write(diretorio, nome_arquivo)
