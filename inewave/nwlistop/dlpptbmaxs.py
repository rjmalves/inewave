from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.dlpptbmaxs import DLPPtbmaxAnos


class DLPPtbmaxs(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à violação das restrições
    LPP de turbinamento máximo por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dlpptbmaxs.out`.
    """

    BLOCKS = [
        DLPPtbmaxAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="dlpptbmaxs.out"
    ) -> "DLPPtbmaxs":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="dlpptbmaxs.out"):
        self.write(diretorio, nome_arquivo)
