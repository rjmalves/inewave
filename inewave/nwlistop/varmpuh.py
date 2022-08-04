from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousina import (
    ArquivoUsina,
)
from inewave.nwlistop.modelos.varmpuh import VarmAnos


class VarmpUH(ArquivoUsina):
    """
    Armazena os dados das saídas referentes aos armazenamentos em
    percentual por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `varmpuh00x.out`, onde x varia conforme a
    usina em questão.

    """

    BLOCKS = [
        Usina,
        VarmAnos,
    ]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="varmpuh001.out"
    ) -> "VarmpUH":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="varmpuh001.out"):
        self.write(diretorio, nome_arquivo)
