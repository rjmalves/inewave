from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)
from inewave.nwlistop.modelos.ghmaxmr import GHAnos


class Ghmaxmr(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes à geração hidraulica máxima
    considerando restrições elétricas por patamar, por Submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ghmaxmr00x.out`, onde x varia conforme o
    Submercado em questão.

    """

    BLOCKS = [
        Submercado,
        GHAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="ghmaxmr001.out"
    ) -> "Ghmaxmr":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="ghmaxmr001.out"):
        self.write(diretorio, nome_arquivo)
