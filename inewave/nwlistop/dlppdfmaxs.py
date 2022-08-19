from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.dlppdfmaxs import DLPPdfmaxAnos


class DLPPdfmaxs(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à violação das restrições
    LPP de defluência máxima por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dlppdfmaxs.out`.
    """

    BLOCKS = [
        DLPPdfmaxAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="dlppdfmaxs.out"
    ) -> "DLPPdfmaxs":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="dlppdfmaxs.out"):
        self.write(diretorio, nome_arquivo)
