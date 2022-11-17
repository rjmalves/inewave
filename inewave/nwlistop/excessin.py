from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.exces import ExcesAnos


class ExcesSIN(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes ao excesso de energia
    por patamar, para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas no `excessin.out`

    """

    BLOCKS = [
        ExcesAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="excessin.out"
    ) -> "ExcesSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="excessin.out"):
        self.write(diretorio, nome_arquivo)
