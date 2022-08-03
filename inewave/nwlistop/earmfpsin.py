from inewave.nwlistop.modelos.earmfpsin import EarmsAnos

from inewave.nwlistop.modelos.arquivos.arquivosin import (
    ArquivoSIN,
)


class EarmfpSIN(ArquivoSIN):
    """
    Armazena os dados das saídas referentes às energias
    armazenadas finais para o SIN e em % da energia armazenável máxima.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `earmfpsin.out`, onde x varia conforme o
    submercado em questão.
    """

    BLOCKS = [
        EarmsAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="earmfpsin.out"
    ) -> "EarmfpSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="earmfpsin.out"):
        self.write(diretorio, nome_arquivo)
