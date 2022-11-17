from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.vghminuh import VGhminuhAnos


class VghminUH(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à violação da meta de
    geração hidráulica mínima por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vghminuh00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        VGhminuhAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="vghminuh001.out"
    ) -> "VghminUH":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="vghminuh001.out"):
        self.write(diretorio, nome_arquivo)
