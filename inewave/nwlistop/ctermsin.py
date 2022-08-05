from inewave.nwlistop.modelos.ctermsin import CtermsAnos
from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)


class CtermSIN(ArquivoSIN):
    """
    Armazena os dados das saídas referentes aos custos de geração térmica
    para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ctermsin.out`.

    """

    BLOCKS = [
        CtermsAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="ctermsin.out"
    ) -> "CtermSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="ctermsin.out"):
        self.write(diretorio, nome_arquivo)
