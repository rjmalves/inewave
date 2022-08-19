from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)
from inewave.nwlistop.modelos.vevminm import VevminAnos


class Vevminm(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes às violações da meta
    de energia da vazão mínima, por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vevminm00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        VevminAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="vevminm001.out"
    ) -> "Vevminm":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="vevminm001.out"):
        self.write(diretorio, nome_arquivo)
