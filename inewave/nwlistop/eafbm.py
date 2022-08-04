from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)
from inewave.nwlistop.modelos.eafbm import EafsAnos


class Eafbm(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes às energias
    afluentes brutas, por submercado em valores absolutos.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `eafbm00x.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        EafsAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="eafbm001.out"
    ) -> "Eafbm":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="eafbm001.out"):
        self.write(diretorio, nome_arquivo)
