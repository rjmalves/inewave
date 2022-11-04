from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.dtbmax import DtbmaxAnos


class Dtbmax(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à violação de restrição de
    turbinamento máximo por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dtbmax00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        DtbmaxAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="dtbmax001.out"
    ) -> "Dtbmax":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="dtbmax001.out"):
        self.write(diretorio, nome_arquivo)
