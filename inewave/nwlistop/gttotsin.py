from inewave.nwlistop.modelos.gttotsin import GTAnos
from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)


class GttotSIN(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à geração térmica total
    por patamar, para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `gttotsin.out`.
    """

    BLOCKS = [
        GTAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="gttotsin.out"
    ) -> "GttotSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="gttotsin.out"):
        self.write(diretorio, nome_arquivo)
