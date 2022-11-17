from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.exces import ExcesAnos


class FteolSIN(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à folga da variável de
    geração eólica para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `fteolsin.out`

    """

    BLOCKS = [
        ExcesAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="fteolsin.out"
    ) -> "FteolSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="fteolsin.out"):
        self.write(diretorio, nome_arquivo)
