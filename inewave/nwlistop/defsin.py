from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.defsin import DefAnos


class DefSIN(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes ao déficit
    por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `defsinp001.out`.
    """

    BLOCKS = [
        DefAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="defsinp001.out"
    ) -> "DefSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="defsinp001.out"):
        self.write(diretorio, nome_arquivo)
