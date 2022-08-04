from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoreepatamar import (
    ArquivoREEPatamar,
)
from inewave.nwlistop.modelos.ghmaxr import GHAnos


class Ghmaxr(ArquivoREEPatamar):
    """
    Armazena os dados das saídas referentes à geração hidraulica máxima
    considerando restrições elétricas por patamar, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ghmax00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        GHAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="ghmaxr001.out"
    ) -> "Ghmaxr":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="ghmaxr001.out"):
        self.write(diretorio, nome_arquivo)
