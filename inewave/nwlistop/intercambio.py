from inewave.nwlistop.modelos.blocos.parsubmercados import ParSubmercados
from inewave.nwlistop.modelos.arquivos.arquivoparsubmercadopatamar import (
    ArquivoParSubmercadoPatamar,
)
from inewave.nwlistop.modelos.intercambio import IntercambioAnos


class Intercambio(ArquivoParSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes ao intercâmbio
    por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `int00x00y.out`, onde x e y variam
    conforme os submercados em questão.

    """

    BLOCKS = [
        ParSubmercados,
        IntercambioAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="int001002.out"
    ) -> "Intercambio":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="ghtotm001.out"):
        self.write(diretorio, nome_arquivo)
