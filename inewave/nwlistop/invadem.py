from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)
from inewave.nwlistop.modelos.invade import InvadeAnos


class Invadem(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes às violações da CAR
    , por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `invadem00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        Submercado,
        InvadeAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="invadem001.out"
    ) -> "Invadem":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="invadem001.out"):
        self.write(diretorio, nome_arquivo)
