from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.geolm import GEAnos


class Geolm(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes à geração eólica total
    por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `geol00x.out`, onde x varia conforme o
    PEE em questão.

    """

    BLOCKS = [
        Submercado,
        GEAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="geolm001.out"
    ) -> "Geolm":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="geolm001.out"):
        self.write(diretorio, nome_arquivo)
