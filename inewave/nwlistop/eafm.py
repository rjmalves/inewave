from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)
from inewave.nwlistop.modelos.eafm import EafsAnos


class Eafm(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes às energias
    afluentes, por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `eaf00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        EafsAnos,
    ]

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo="eafm001.out") -> "Eafm":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="eafm001.out"):
        self.write(diretorio, nome_arquivo)
