from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.ctermsin import CtermsAnos
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)


class Cterm(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes aos custos de geração térmica
    por patamar para o SIN.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cterm00x.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        CtermsAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="ctermsin.out"
    ) -> "Cterm":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="ctermsin.out"):
        self.write(diretorio, nome_arquivo)
