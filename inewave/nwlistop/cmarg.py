from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.cmarg import CmargsAnos
from inewave.nwlistop.modelos.arquivos.arquivosubmercadopatamar import (
    ArquivoSubmercadoPatamar,
)


class Cmarg(ArquivoSubmercadoPatamar):
    """
    Armazena os dados das saídas referentes aos custos marginais de operação
    por patamar, por submercado.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `cmarg00x.out`, onde x varia conforme o
    submercado em questão.

    """

    BLOCKS = [
        Submercado,
        CmargsAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="cmarg001.out"
    ) -> "Cmarg":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="cmarg001.out"):
        self.write(diretorio, nome_arquivo)
