from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.arquivos.arquivosubmercado import (
    ArquivoSubmercado,
)
from inewave.nwlistop.modelos.cmargmed import CmargsAnos


class CmargMed(ArquivoSubmercado):
    """
    Armazena os dados das saídas referentes aos custos marginais de operação
    por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cmarg00x-med.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        CmargsAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="cmarg001-med.out"
    ) -> "CmargMed":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="cmarg001-med.out"):
        self.write(diretorio, nome_arquivo)
