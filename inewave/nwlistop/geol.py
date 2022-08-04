from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.geol import GEAnos


class Geol(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à geração eólica total
    por patamar, por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `geol00x.out`, onde x varia conforme o
    PEE em questão.

    """

    BLOCKS = [
        Usina,
        GEAnos,
    ]

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="geol001.out") -> "Geol":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="geol001.out"):
        self.write(diretorio, nome_arquivo)
