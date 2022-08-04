from inewave.nwlistop.modelos.arquivos.arquivosinpatamar import (
    ArquivoSINPatamar,
)
from inewave.nwlistop.modelos.ghmaxrsin import GHAnos


class GhmaxrSIN(ArquivoSINPatamar):
    """
    Armazena os dados das saídas referentes à geração hidraulica máxima
    considerando restrições elétricas por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `ghmaxsin.out`.
    """

    BLOCKS = [
        GHAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="ghmaxrsin.out"
    ) -> "GhmaxrSIN":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="ghmaxrsin.out"):
        self.write(diretorio, nome_arquivo)
